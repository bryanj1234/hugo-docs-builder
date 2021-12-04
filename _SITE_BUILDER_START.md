---
title: 02 Hugo Docs Builder
---

## Make a simple website from a code repository.

I used Hugo Docs Builder to build [this website](https://bryanj1234.github.io) from my [GitHub public repo](https://github.com/bryanj1234/bryanj1234.github.io).

Hugo Docs Builder project folder on GitHub: [Hugo Docs Builder](https://github.com/bryanj1234/hugo-docs-builder).

### Usage

    bash run-hugo-docs-builder.sh {source_code-folder} {html_output_folder}

### How it works

There are three magic file names that control what directory sub-trees will be indexed.

* `_SITE_BUILDER_START.md`  
    Indicates that a directory sub-tree should be indexed.  
    Indexing will start at each directory inside `{source_code-folder}` which contains a `_SITE_BUILDER_START.md` file.  
    Also provides the page title and (optional) content.
* `_SITE_BUILDER_INDEX.md`
    Povides the page title and (optional) content.
* `_SITE_BUILDER_STOP`  
    Prevents indexing directory sub-tree any deeper **for indexing started at or above** the `_SITE_BUILDER_STOP` file,
        but still allows indexing the directory with the file.  
    Does not affect indexing of sub-trees whose `_SITE_BUILDER_START.md` files live deeper than the `_SITE_BUILDER_STOP` file.

### Example


Suppose your source directory looks like this:

<pre>
example_source
├── folder_1
│   └── source_file_XXX.txt
└── <span style="background-color:yellow;color:black">folder_2</span>
    ├── <span style="background-color: green">folder_3</span>
    │   ├── <span style="background-color: green">_SITE_BUILDER_INDEX.md</span>
    │   └── source_file_5.php
    ├── <span style="background-color: blue">folder_4</span>
    │   ├── folder_5
    │   │   └── source_file_6.c
    │   ├── <span style="background-color: blue">_SITE_BUILDER_START.md</span>
    │   └── _SITE_BUILDER_STOP
    ├── <span style="background-color:yellow;color:black">_SITE_BUILDER_START.md</span>
    ├── source_file_A.txt
    ├── source_file_B.html
    └── source_file_C.py
</pre>

Then running

    bash ../run-hugo-docs-builder.sh example_source/ www/

results in this:

<pre>
www
├── index.html
├── _SITE_BUILDER_STOP
├── source_files
│   ├── folder_2
│   │   ├── folder_3
│   │   │   └── source_file_5.php
│   │   ├── source_file_A.txt
│   │   ├── source_file_B.html
│   │   └── source_file_C.py
│   └── _SITE_BUILDER_STOP
├── <span style="background-color:yellow;color:black">My-title-for-source-folder-2</span>
│   ├── <span style="background-color: green">folder_3</span>
│   │   ├── index.html
│   │   └── __wrap__source_file_5.php
│   │       └── index.html
│   ├── folder_4
│   │   ├── index.html
│   ├── index.html
│   ├── __wrap__source_file_a.txt
│   │   └── index.html
│   ├── __wrap__source_file_b.html
│   │   └── index.html
│   └── __wrap__source_file_c.py
│       └── index.html
├── <span style="background-color: blue">My-title-for-source-folder-4</span>
│   ├── index.html
</pre>
