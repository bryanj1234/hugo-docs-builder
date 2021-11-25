import sys
import os
import pathlib

print()
print("##############################################################")
print("##############################################################")
print()
#print(pathlib.Path(__file__).name)
print()
print("Running with Python version", sys.version)
print("Running with Python executable", sys.executable)
print()

import shutil
from bs4 import BeautifulSoup
import frontmatter
import io

####################################################################################################
####################################################################################################
####################################################################################################

# Usage: python hugo_docs_builder.py SOURCE_DIR

####################################################################################################
####################################################################################################
####################################################################################################

def recursive_dir_scan(cur_dir_path_str, cur_contents):
    # Increment level
    level = cur_contents[1]
    level += 1
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
                    child_records = recursive_dir_scan(entry.path, new_rec)
                elif entry.is_file():
                    name_str = entry.name
                    abs_path_str = os.path.abspath(entry.path)
                    # print(" " * 2 * level, level, "file:", name_str, abs_path_str)
                    cur_contents[4].append(["FILE", level, name_str, abs_path_str])

    except (FileNotFoundError):
        print("Directory not found.")
        print("Specify source content directory, relative to the above working directory.")
        sys.exit(1)

    return cur_contents

def recursively_print_and_flatten_dir_contents(current_dir, cur_flat_list, root_path):
    file_or_dir = current_dir[0]    # Always "DIR" for this record...
    level = current_dir[1]
    name_str = current_dir[2]
    abs_path_str = current_dir[3]
    child_recs = current_dir[4]
    rel_path_str = os.path.relpath(abs_path_str, root_path)

    print("X" * 2 * level, level, file_or_dir, name_str)

    cur_flat_list.append([file_or_dir, level, name_str, abs_path_str, rel_path_str])

    for child_rec in child_recs:
        file_or_dir = child_rec[0]
        level = child_rec[1]
        name_str = child_rec[2]
        abs_path_str = current_dir[3]
        rel_path_str = os.path.relpath(abs_path_str, root_path)

        if file_or_dir == "FILE":
            _, file_extension = os.path.splitext(name_str)
            file_extension = file_extension.upper().replace(".", "")

            #print(" " * 2 * level, level, file_or_dir, name_str, file_extension)

            cur_flat_list.append([file_or_dir, level, name_str, abs_path_str, rel_path_str])
        else: # "DIR"
            recursively_print_and_flatten_dir_contents(child_rec, cur_flat_list, root_path)

    return cur_flat_list

def index_file_exists(new_abs_dir_path_str):
    index_html_str = os.path.join(new_abs_dir_path_str, "index.html")
    index_htm_str = os.path.join(new_abs_dir_path_str, "index.htm")
    index_md_str = os.path.join(new_abs_dir_path_str, "_index.md")
    index_md_str_2 = os.path.join(new_abs_dir_path_str, "index.md")
    return pathlib.Path(index_html_str).is_file() or pathlib.Path(index_htm_str).is_file() \
            or pathlib.Path(index_md_str).is_file() or pathlib.Path(index_md_str_2).is_file()

def make_index_file_if_necessary(new_abs_dir_path_str):
    # Add _index.md file for Hugo, BUT ONLY IF NOT ALREADY PRESENT. DON'T WANT TO CLOBBER ONE GENERATED FROM README.
    if not index_file_exists(new_abs_dir_path_str):
        index_file_str = os.path.join(new_abs_dir_path_str, "_index.md")
        with open(index_file_str, 'w') as the_file:
            dir_name = pathlib.Path(new_abs_dir_path_str).name
            the_file.write('---\nTitle: ' + dir_name + '\n---\n')

def make_dir_if_necessary(new_abs_dir_path_str):

    dir_name = pathlib.Path(new_abs_dir_path_str).name

    # Make new directory, with parents, if necessary.
    pathlib.Path(new_abs_dir_path_str).mkdir(parents=True, exist_ok=True)

def make_new_file(new_abs_dir_path_str, new_abs_file_path_str, old_abs_file_path_str):

    # Skip files that result it frontmatter module errors, for example when a markdown file contains problematic backslashes.
    try:

        bool_created_file = False

        file_name = pathlib.Path(old_abs_file_path_str).name
        dir_name = pathlib.Path(new_abs_dir_path_str).name

        _, file_extension = os.path.splitext(old_abs_file_path_str)
        file_extension = file_extension.upper().replace(".", "")

        # START File handling depends on extension. ##########################################################
        if file_name.upper() == "README.MD":       # MAGIC. README files are converted into _index.md files.
            bool_created_file = True

            # NOTE: README files are converted into _index.md files.
            # Write the new _index.mf file.
            # Deal with frontmatter that Hugo needs to work right.
            #
            # Don't clobber an index.html file though.
            with open(old_abs_file_path_str, 'r') as f:
                post = frontmatter.loads(f.read())
                f.close()
                if not 'title' in post:
                    post['title'] = file_name
                index_file_str = os.path.join(new_abs_dir_path_str, "_index.md")
                with open(index_file_str, 'w') as f:
                    f.write(frontmatter.dumps(post))

        # elif file_extension == "HTML":   # MAGIC
        #     bool_created_file = True

        #     shutil.copyfile(old_abs_file_path_str, new_abs_file_path_str)
        #     # Also make a new file "__MD_" + new_abs_file_path_str + ".md" which shows the HTML in an iframe.
        #     new_file_md_str = "__MD_" + file_name + ".md"
        #     new_file_md_abs_path_str = os.path.join(new_abs_dir_path_str, new_file_md_str)

        #     # Get the page title.
        #     title_str = file_name

        #     with open(new_file_md_abs_path_str, 'w') as the_file:
        #         the_file.write('---\nTitle: ' + title_str + '\n---\n\n')
        #         # !!! NOTE !!! The "../" in the next line is because of what Hugo does when it processes files and directories.
        #         write_str = '<iframe width="100%" name="iframe" src= "../' + file_name + '" frameborder="0" scrolling="no" onload="resizeIframe(this)"></iframe>'
        #         the_file.write(write_str + '\n')
        #         write_str = "<script> function resizeIframe(obj) {obj.style.height = obj.contentWindow.document.body.scrollHeight + 'px';}</script>"
        #         the_file.write(write_str + '\n')
        #         #print(new_file_md_abs_path_str)

        # elif file_extension == "MP4":   # MAGIC, similar to the HTML handler.
        #     bool_created_file = True

        #     shutil.copyfile(old_abs_file_path_str, new_abs_file_path_str)
        #     new_file_md_str = "__MD_" + file_name + ".md"
        #     new_file_md_abs_path_str = os.path.join(new_abs_dir_path_str, new_file_md_str)

        #     # Get the page title.
        #     title_str = file_name

        #     with open(new_file_md_abs_path_str, 'w') as the_file:
        #         the_file.write('---\nTitle: ' + title_str + '\n---\n\n')
        #         # !!! NOTE !!! The "../" in the next line is because of what Hugo does when it processes files and directories.
        #         write_str = '<center><video width="70%" controls autoplay><source src="../' + file_name + '" type="video/mp4">Your browser does not support the video tag.</video></center>'
        #         the_file.write(write_str + '\n')

        # elif file_extension == "PY" or file_extension == "CSD" :   # MAGIC
        #     bool_created_file = True

        #     new_file_md_str = "__MD_" + file_name + ".md"
        #     new_file_md_abs_path_str = os.path.join(new_abs_dir_path_str, new_file_md_str)
        #     with open(old_abs_file_path_str, 'r') as f:
        #         post = frontmatter.loads(f.read())
        #         post['title'] = file_name
        #         post.content = "```\n" + post.content + "\n```"
        #         f.close()
        #         with open(new_file_md_abs_path_str, 'w') as f:
        #             f.write(frontmatter.dumps(post))

        else: # COPY.
            bool_created_file = True
            shutil.copyfile(old_abs_file_path_str, new_abs_file_path_str)

        # END File handling depends on extension. ##########################################################

        # Add an index file if necessary
        if bool_created_file:
            make_index_file_if_necessary(new_abs_dir_path_str)

    except Exception as error:
        print()
        print("*** ERROR")
        print("    ", repr(error))
        print("Skipping source file ", old_abs_file_path_str)
        print()

def process_flattened_list(flat_list, output_content_dir_path_str):

    # Remove and recreate the output directory.

    #print(output_content_dir_path_str)
    shutil.rmtree(output_content_dir_path_str, ignore_errors=True)
    os.mkdir(output_content_dir_path_str)

    # Maybe use os.path.join('/my/root/directory', 'in', 'here')

    for rec in flat_list:
        #print(rec) # [file_or_dir, level, name_str, abs_path_str, rel_path_str]

        file_or_dir = rec[0]
        level = rec[1]
        name_str = rec[2]
        orig_abs_path_str = rec[3]
        rel_path_str = rec[4]

        if file_or_dir == "FILE":
            # Get old absolute path
            old_abs_file_path_str = os.path.join(orig_abs_path_str, name_str)
            #print("OLD:", old_abs_file_path_str)

            # Make new absolute path
            new_abs_dir_path_str = os.path.join(output_content_dir_path_str, rel_path_str)
            new_abs_file_path_str = os.path.join(output_content_dir_path_str, rel_path_str, name_str)
            #print("NEW DIR:", new_abs_dir_path_str)
            #print("NEW FILE:", new_abs_file_path_str)

            # Make a new directory if you need to.
            make_dir_if_necessary(new_abs_dir_path_str)

            # Make new file
            make_new_file(new_abs_dir_path_str, new_abs_file_path_str, old_abs_file_path_str)

        else: # "DIR"
            # Make new absolute path
            new_abs_dir_path_str = os.path.join(output_content_dir_path_str, rel_path_str)
            #print("NEW DIR:", new_abs_dir_path_str)
            # Make a new directory if you need to.
            make_dir_if_necessary(new_abs_dir_path_str)



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

    print("Source content directory: ", source_content_dir_path_str)
    print("Output content directory: ", output_content_dir_path_str)
    print()
    print("Processing source directory...")

    # Recursively scan the direstory.

    dir_contents = recursive_dir_scan(source_content_dir_path_str, ['DIR', 0, 'XXX_ROOT_XXX', source_content_dir_path_str, []])

    # print("##############################################################")
    # print("Source content directory structure")
    # print("##############################################################")
    # print()

    flat_list = recursively_print_and_flatten_dir_contents(dir_contents, [], source_content_dir_path_str)

    process_flattened_list(flat_list, output_content_dir_path_str)

    print("Done creating new files.")
    print()

    print("##############################################################")
    print("##############################################################")

    print()

except Exception as error:
    print()
    print("*** ERROR")
    print("    ", repr(error))
    sys.exit(1)