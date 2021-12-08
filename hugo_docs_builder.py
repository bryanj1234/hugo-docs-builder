import sys
import os
import pathlib
import traceback
import shutil
from bs4 import BeautifulSoup
import frontmatter
import io

print()
print("##############################################################")
print("##############################################################")
print()
#print(pathlib.Path(__file__).name)
print()
print("Running with Python version", sys.version)
print("Running with Python executable", sys.executable)
print()

####################################################################################################
####################################################################################################
####################################################################################################

# Usage: python hugo_docs_builder.py SOURCE_DIR

####################################################################################################
####################################################################################################
####################################################################################################

# INCREASE PERFORMANCE
dict_index_files_made = {}
dict_entry_point_info = {}

def recursive_find_site_builder_start(cur_dir_path_str, entry_points_list):

    try:
        with os.scandir(cur_dir_path_str) as it:
            for entry in it:
                if entry.is_dir():
                    recursive_find_site_builder_start(entry.path, entry_points_list)
                elif entry.is_file():
                    name_str = entry.name
                    abs_path_str = os.path.abspath(entry.path)

                    # Look for _SITE_BUILDER_START.md
                    if name_str == "_SITE_BUILDER_START.md":
                        dir_path = os.path.dirname(os.path.realpath(abs_path_str))
                        entry_points_list.append([dir_path, name_str])

    except (FileNotFoundError):
        print("Directory not found.")
        print("Specify source content directory, relative to the above working directory.")
        sys.exit(1)

# FIXME: Use a dictionary for lookup. This is way too much file I/O.
def DOCBUILDER_index_file_exists(content_dir_abs_path_str):
    index_str = os.path.join(content_dir_abs_path_str, "_index.md")

    # Test both, but use short-circuiting.
    bool_index_exists = (index_str in dict_index_files_made) or pathlib.Path(index_str).is_file()

    return bool_index_exists

# Recursively adds missing _index.md files from output_content_dir_path_str to cur_dir.
# Use a dictionary for lookup to prevent too much file I/O.
def make_DOCBUILDER_index_files_if_necessary(output_content_dir_path_str, cur_dir):
    cur_dir = pathlib.Path(cur_dir).absolute()

    # Add _index.md file for Hugo, BUT ONLY IF NOT ALREADY PRESENT. DON'T WANT TO CLOBBER ONE GENERATED FROM README.
    if not DOCBUILDER_index_file_exists(cur_dir):
        index_file_str = os.path.join(cur_dir, "_index.md")
        with open(index_file_str, 'w') as the_file:
            dir_name = pathlib.Path(cur_dir).name
            the_file.write('---\n')
            the_file.write('title: ' + dir_name + '\n')
            the_file.write('type:   HDBfolder\n')
            the_file.write('---\n')


            # Add to list of index files already made.
            dict_index_files_made[cur_dir] = True

    parent_dir = pathlib.Path(cur_dir).parent.absolute()
    if not parent_dir == pathlib.Path(output_content_dir_path_str).absolute():
        make_DOCBUILDER_index_files_if_necessary(output_content_dir_path_str, parent_dir)

def recursive_dir_scan(cur_dir_path_str, cur_contents):
    # Increment level
    level = cur_contents[1]
    level += 1

    # Check to see if we should stop recursion prematurely.
    # This is determined by the presence of a _SITE_BUILDER_STOP file (no extension, case sensitive).
    stop_file_str = os.path.join(cur_dir_path_str, "_SITE_BUILDER_STOP")
    bool_stop_file_exists = os.path.exists(stop_file_str)

    try:
        with os.scandir(cur_dir_path_str) as it:
            for entry in it:
                if entry.is_dir():
                    name_str = entry.name
                    abs_path_str = os.path.abspath(entry.path)

                    # print("X" * 2 * level, level, "directory:", name_str, abs_path_str)
                    # print(" " * 2* level, "(recursing)")
                    new_rec = ["DIR", level, name_str, abs_path_str, []]
                    cur_contents[4].append(new_rec)

                    if bool_stop_file_exists:
                        print("Found stop file", stop_file_str)
                        print("Not recursing.")
                    else:
                        child_records = recursive_dir_scan(entry.path, new_rec)

                elif entry.is_file():
                    name_str = entry.name
                    abs_path_str = os.path.abspath(entry.path)
                    #print(" " * 2 * level, level, "file:", name_str, abs_path_str)
                    cur_contents[4].append(["FILE", level, name_str, abs_path_str])

    except (FileNotFoundError):
        print("Directory not found.")
        print("Specify source content directory, relative to the above working directory.")
        sys.exit(1)

    return cur_contents

def recursively_print_and_flatten_dir_contents(current_dir, cur_flat_list, source_content_dir_path_str, entry_point_dir):
    file_or_dir = current_dir[0]    # Always "DIR" for this record...
    level = current_dir[1]
    name_str = current_dir[2]
    abs_path_str = current_dir[3]
    child_recs = current_dir[4]

    #print("X" * 2 * level, level, file_or_dir, name_str)

    source_rel_dir_path_str = os.path.relpath(abs_path_str, source_content_dir_path_str)
    entry_rel_dir_path_str = os.path.relpath(abs_path_str, entry_point_dir)

    cur_flat_list.append([file_or_dir, level, name_str, abs_path_str, source_rel_dir_path_str, entry_rel_dir_path_str])

    for child_rec in child_recs:
        file_or_dir = child_rec[0]
        level = child_rec[1]
        name_str = child_rec[2]
        abs_path_str = current_dir[3]

        if file_or_dir == "FILE":
            _, file_extension = os.path.splitext(name_str)
            file_extension = file_extension.upper().replace(".", "")

            #print(" " * 2 * level, level, file_or_dir, name_str, file_extension)

            source_rel_dir_path_str = os.path.relpath(abs_path_str, source_content_dir_path_str)
            entry_rel_dir_path_str = os.path.relpath(abs_path_str, entry_point_dir)

            cur_flat_list.append([file_or_dir, level, name_str, abs_path_str, source_rel_dir_path_str, entry_rel_dir_path_str])
        else: # "DIR"
            recursively_print_and_flatten_dir_contents(child_rec, cur_flat_list, source_content_dir_path_str, entry_point_dir)

    return cur_flat_list

def make_dir_if_necessary(dir_abs_path_str):

    # Make new directory, with parents, if necessary.
    pathlib.Path(dir_abs_path_str).mkdir(parents=True, exist_ok=True)


def make_new_file(new_file_info):

    # new_file_info = {
    #     'output_content_dir_path_str': output_content_dir_path_str,
    #     'content_dir_abs_path_str': content_dir_abs_path_str,
    #     'source_file_abs_path_str': source_file_abs_path_str,
    #     'source_file_rel_path_str': source_file_rel_path_str,
    #     'output_static_dir_path_str': output_static_dir_path_str,
    #     'publish_static_source_dir_str': publish_static_source_dir_str,
    #     'source_dir_path_str': source_dir_path_str,
    #     'source_file_path_str': source_file_path_str
    # }

    output_content_dir_path_str = new_file_info['output_content_dir_path_str']
    content_dir_abs_path_str = new_file_info['content_dir_abs_path_str']
    source_file_abs_path_str = new_file_info['source_file_abs_path_str']
    source_file_rel_path_str = new_file_info['source_file_rel_path_str']
    output_static_dir_path_str = new_file_info['output_static_dir_path_str']
    publish_static_source_dir_str = new_file_info['publish_static_source_dir_str']
    source_dir_path_str = new_file_info['source_dir_path_str']
    source_file_path_str = new_file_info['source_file_path_str']

    # Make a new directory in the content folder if you need to.
    make_dir_if_necessary(content_dir_abs_path_str)

    # Add an index files if necessary
    make_DOCBUILDER_index_files_if_necessary(output_content_dir_path_str, content_dir_abs_path_str)

    # Skip files that result it frontmatter module errors, for example when a markdown file contains problematic backslashes.
    try:

        file_name = pathlib.Path(source_file_abs_path_str).name

        file_base_name, file_extension = os.path.splitext(file_name)

        file_extension = file_extension.upper().replace(".", "")

        # START File handling depends on file name. ##########################################################

        if file_name == "_SITE_BUILDER_START.md" \
                or file_name == "_SITE_BUILDER_INDEX.md":

            # print("\n***********************************************************")
            # print(content_dir_abs_path_str)
            # print(source_file_abs_path_str)
            # print(source_file_rel_path_str)
            # print(output_static_dir_path_str)
            # print(publish_static_source_dir_str)
            # print("\n***********************************************************")

            # NOTE: _SITE_BUILDER_START.md files are converted into _index.md files.
            # Write the new _index.md file.
            # Deal with frontmatter that Hugo needs to work right.
            with open(source_file_abs_path_str, 'r') as f:
                post = frontmatter.loads(f.read())
                f.close()

                if not 'title' in post:
                    exception_str = '_SITE_BUILDER file ' + source_file_abs_path_str + ' needs title.'
                    raise Exception(exception_str)

                # Determine if we need to add extra info for rendering html AS HTML instead of as a source file...
                if 'render_html_file' in post:
                    source_file_rel_dir_str = pathlib.Path(source_file_rel_path_str).parent
                    post['source_file_full_name'] = os.path.join('/', publish_static_source_dir_str, source_file_rel_dir_str, post['render_html_file'])


                index_file_str = os.path.join(content_dir_abs_path_str, "_index.md")
                with open(index_file_str, 'w') as f:
                    f.write(frontmatter.dumps(post))
                    # Add to list of index files already made.
                    dict_index_files_made[content_dir_abs_path_str] = True

        elif file_name == '_SITE_BUILDER_STOP':
            pass

        elif file_extension == '_SB_':  # The file should be processed as markdown, not source.

            # Copy file, rename, and remove original.
            new_content_file_name_str = os.path.join(content_dir_abs_path_str, file_base_name)
            shutil.copyfile(source_file_abs_path_str, new_content_file_name_str)

        else: # Treat as a code source file in /static/source_files and wrap it up in a *.md file...

            # Copy the original file to the static source directory

            # Make a new directory if you need to.
            make_dir_if_necessary(source_dir_path_str)

            # Copy file
            shutil.copyfile(source_file_abs_path_str, source_file_path_str)

            # Wrap up the file to put into the content directory
            wrapper_md_file_path_str = os.path.join(content_dir_abs_path_str, '__WRAP__' + file_name + ".md")

            with open(wrapper_md_file_path_str, 'w') as the_file:
                the_file.write('---')
                the_file.write('\nTitle: ' + file_name)
                the_file.write('\ntype: HDBsourcefile')
                the_file.write('\nis_source_file: true')
                the_file.write('\nsource_file_name: ' + file_name)
                the_file.write('\nsource_file_rel_name: ' + source_file_rel_path_str)
                the_file.write('\nsource_file_hugo_full_name: ' + os.path.join('/',output_static_dir_path_str, source_file_rel_path_str))
                the_file.write('\nsource_file_full_name: ' + os.path.join('/',publish_static_source_dir_str, source_file_rel_path_str))
                the_file.write('\nsource_file_ext: ' + file_extension)
                the_file.write('\n---')
                the_file.write('\n\n')


        # END File handling depends on file name. ##########################################################

    except Exception as error:
        print()
        print("*** ERROR")
        print("    ", repr(error))
        print("Skipping source file ", source_file_abs_path_str)
        traceback.print_exc()
        sys.exit(1)

def get_entry_point_info(source_file_abs_path_str):

    entry_point_info = False
    if source_file_abs_path_str in dict_entry_point_info:
        entry_point_info = dict_entry_point_info[source_file_abs_path_str]
    else:
        with open(source_file_abs_path_str, 'r') as f:
            post = frontmatter.loads(f.read())
            f.close()
            entry_point_info = {}
            if 'title' in post:
                entry_point_info['title'] = post['title']
            else:
                exception_str = '_SITE_BUILDER file ' + source_file_abs_path_str + ' needs title.'
                raise Exception(exception_str)
            if 'top_level_category_override' in post:
                entry_point_info['top_level_category_override'] = post['top_level_category_override']

    return entry_point_info

def process_flattened_list(flat_lists, output_content_dir_path_str, output_static_dir_path_str, publish_static_source_dir_str):

    for entry_point_rec in flat_lists:

        entry_point_dir_str = entry_point_rec["entry_point_dir_str"]
        entry_point_file_str = entry_point_rec["entry_point_file_str"]

        # Get entry point into from entry point start file...
        # FIXME: Use a dictionary for lookup. This is way too much file I/O.
        source_file_abs_path_str = os.path.join(entry_point_dir_str, entry_point_file_str)
        entry_point_info = get_entry_point_info(source_file_abs_path_str)
        entry_point_title_str = entry_point_info['title']
        top_level_category_override_str = ''
        if 'top_level_category_override' in entry_point_info:
            top_level_category_override_str = entry_point_info['top_level_category_override']

        flat_list = entry_point_rec["flat_list"]
        for rec in flat_list:

            # print("entry_point_dir_str:", entry_point_dir_str)
            # print("        ", rec) # [file_or_dir, level, name_str, abs_path_str, source_rel_dir_path_str, entry_rel_dir_path_str]
            #         # ['FILE', 2, 'vcs.xml', '/home/bryan/Documents/DEV/version-controlled/bryanj1234.github.io/projects/DS/Google-MLCC/.idea',
            #         #               'DS/Google-MLCC/.idea', '.idea']
            #         # ['DIR', 1, '.idea', '/home/bryan/Documents/DEV/version-controlled/bryanj1234.github.io/projects/DS/Google-MLCC/.idea',
            #         #               'DS/Google-MLCC/.idea', '.idea']

            file_or_dir = rec[0]
            level = rec[1]
            name_str = rec[2]
            dir_abs_path_str = rec[3]
            dir_rel_source_dir_str = rec[4]
            dir_rel_entry_point_dir_str = rec[5]

            if file_or_dir == "FILE":

                # Get old absolute path
                source_file_abs_path_str = os.path.join(dir_abs_path_str, name_str)

                # Make new content path
                content_dir_abs_path_str = os.path.join(output_content_dir_path_str, top_level_category_override_str, entry_point_title_str, dir_rel_entry_point_dir_str)

                # Make static source path
                source_dir_path_str = os.path.join(output_static_dir_path_str, dir_rel_source_dir_str)
                source_file_path_str = os.path.join(source_dir_path_str, name_str)
                source_file_rel_path_str = os.path.join(dir_rel_source_dir_str, name_str)

                # Make new file
                new_file_info = {
                    'output_content_dir_path_str': output_content_dir_path_str,
                    'content_dir_abs_path_str': content_dir_abs_path_str,
                    'source_file_abs_path_str': source_file_abs_path_str,
                    'source_file_rel_path_str': source_file_rel_path_str,
                    'output_static_dir_path_str': output_static_dir_path_str,
                    'publish_static_source_dir_str': publish_static_source_dir_str,
                    'source_dir_path_str': source_dir_path_str,
                    'source_file_path_str': source_file_path_str
                }
                make_new_file(new_file_info)

            else: # "DIR"
                # Nothing to do here, since will make directories only as needed when creating files...
                pass

####################################################################################################
####################################################################################################
####################################################################################################

try:

    working_dir_str = os.getcwd()
    print("Working directory: ", working_dir_str)

    print()

    print("Checking arguments:")

    if len(sys.argv[1:]) != 1:
        print("Usage: python hugo_docs_builder.py SOURCE_DIR")
        sys.exit(1)

    # FOR REAL
    source_content_dir_path_str = os.path.join(working_dir_str, sys.argv[1])
    # FOR TESTING
    #source_content_dir_path_str = "/home/bryan/Documents/Repositories/bryanj1234.github.io/projects"

    # Output directory is the one in the Hugo site template.
    output_content_dir_path_str = os.path.join(str(pathlib.Path(__file__).parent), 'site-hugo-template/content')
    output_public_dir_path_str = os.path.join(str(pathlib.Path(__file__).parent), 'site-hugo-template/public')
    output_static_dir_path_str = os.path.join(str(pathlib.Path(__file__).parent), 'site-hugo-template', 'static/source_files')
    publish_static_source_dir_str = "/source_files"

    print("Source content directory: ", source_content_dir_path_str)
    print("Output content directory: ", output_content_dir_path_str)
    print("Output public directory: ", output_public_dir_path_str)
    print("Output static source directory: ", output_static_dir_path_str)
    print()

    # Remove and recreate the output directories.
    # Also make _SITE_BUILDER_STOP to avoid recursion.

    # content
    shutil.rmtree(output_content_dir_path_str, ignore_errors=True)
    os.mkdir(output_content_dir_path_str)
    pathlib.Path(os.path.join(output_content_dir_path_str, '_SITE_BUILDER_STOP')).touch()

    # public
    shutil.rmtree(output_content_dir_path_str, ignore_errors=True)
    os.mkdir(output_content_dir_path_str)
    pathlib.Path(os.path.join(output_content_dir_path_str, '_SITE_BUILDER_STOP')).touch()

    # static source
    shutil.rmtree(output_static_dir_path_str, ignore_errors=True)
    os.mkdir(output_static_dir_path_str)
    pathlib.Path(os.path.join(output_static_dir_path_str, '_SITE_BUILDER_STOP')).touch()

    print("Processing source directory...")

    # Find entry points for site builder.
    entry_points_list = []
    recursive_find_site_builder_start(source_content_dir_path_str, entry_points_list)

    flat_lists = []
    for rec in entry_points_list:

        entry_point_dir = rec[0]
        entry_point_file = rec[1]

        # Recursively scan the directory.
        dir_contents = recursive_dir_scan(entry_point_dir, ['DIR', 0, entry_point_dir, entry_point_dir, []])
        entry_point_flat_list = recursively_print_and_flatten_dir_contents(dir_contents, [], source_content_dir_path_str, entry_point_dir)
        entry_point_rec = {"entry_point_dir_str": entry_point_dir, "entry_point_file_str": entry_point_file, "flat_list": entry_point_flat_list}

        flat_lists.append(entry_point_rec)

    process_flattened_list(flat_lists, output_content_dir_path_str, output_static_dir_path_str, publish_static_source_dir_str)

    print("Done creating new files.")
    print()

    print("##############################################################")
    print("##############################################################")

    print()

except Exception as error:
    print()
    print("*** ERROR")
    print("    ", repr(error))
    traceback.print_exc()
    sys.exit(1)