---
title: Hugo Docs Builder
---

## Make a simple website from a code repository.

I used Hugo Docs Builder to build this website from my [GitHub public repo](https://github.com/bryanj1234/bryanj1234.github.io).

Hugo Docs Builder project folder on GitHub: [Hugo Docs Builder](https://github.com/bryanj1234/hugo-docs-builder).

### Usage

    bash run-hugo-docs-builder.sh {source_code-folder} {html_output_folder}

### What it does

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


        my_project_root
        │   foo1.md
        │   bar1.txt
        │
        └───folder1
        │   │   _SITE_BUILDER_START.md
        │   │   foo2.txt
        │   │   bar2.txt
        │   │
        │   └───subfolderA
        │       │   foo3.txt
        │       │   bar3.txt
        │       │   
        │       └───subfolderB
        │           │   _SITE_BUILDER_INDEX.md
        │           │   _SITE_BUILDER_STOP
        │           │   foo4.txt
        │           │   bar4.txt
        │           │   ...
        │
        └───folder2
            │   _SITE_BUILDER_START.md
            │   foo4.txt
            │   ...
