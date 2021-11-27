#!/bin/bash

# ARG_1 is the source content directory

CURRENT_WD=$PWD;

echo

if [ $# -ne 2 ];
    then
        echo "Aborting."
        echo "    There should be exactly two argument, the source content directory and the output docs directory."
        echo "Usage:"
        echo "    bash run-hugo-docs-builder.sh SOURCE_DIR OUTPUT_DOCS_DIR."
        exit 1
fi

SOURCE_DIR="$(cd "$(dirname "${1}")"; pwd)/$(basename "${1}")";
OUTPUT_DOCS_DIR="$(cd "$(dirname "${2}")"; pwd)/$(basename "${2}")";


echo "================================================================================="
echo "================================================================================="
echo "================================================================================="
echo
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
echo "This script lives in ${SCRIPT_DIR}.";
echo
echo "Using source content directory: ${SOURCE_DIR}.";
echo "Using output docs directory: ${OUTPUT_DOCS_DIR}.";
echo

HUGO="${SCRIPT_DIR}/site-hugo-template"
CONTENT="${SCRIPT_DIR}/site-hugo-template/content"
STATICSOURCE="${SCRIPT_DIR}/site-hugo-template/static/source_files"
PUBLIC="${SCRIPT_DIR}/site-hugo-template/public"

echo "Removing and remaking content folder from PREVIOUS Hugo run."
rm -fr $CONTENT
mkdir -p $CONTENT
# Prevent Hugo Docs Builder from recursing into this directory.
touch "${CONTENT}/_SITE_BUILDER_STOP"

echo "Removing and remaking static source folder from PREVIOUS Hugo run."
rm -fr $STATICSOURCE
mkdir -p $STATICSOURCE
# Prevent Hugo Docs Builder from recursing into this directory.
touch "${STATICSOURCE}/_SITE_BUILDER_STOP"

echo "Removing and remaking public folder from PREVIOUS Hugo run."
rm -fr $PUBLIC
mkdir -p $PUBLIC
# Prevent Hugo Docs Builder from recursing into this directory.
touch "${PUBLIC}/_SITE_BUILDER_STOP"

echo "Prevent Hugo Docs Builder from recursing into output docs directory."
touch "${OUTPUT_DOCS_DIR}/_SITE_BUILDER_STOP"

echo "Running ${SCRIPT_DIR}/hugo_docs_builder.py ${SOURCE_DIR}..."

python "${SCRIPT_DIR}/hugo_docs_builder.py" $SOURCE_DIR

if [ $? -ne 0 ]; then
    echo
    echo "Aborting."
    echo "hugo_docs_builder.py failed."
    echo "See output for details."
    exit 1
fi

echo
echo "Current working directory: ${CURRENT_WD}".
echo "Changing working directory to ${HUGO}."
cd $HUGO
echo "Working directory: ${PWD}"
echo

echo "Running hugo -D"

hugo -D

#exit

# Can't delete and rebuild the output docs directory because it might have version control info in it.

echo
echo "Changing working directory to ${OUTPUT_DOCS_DIR}."
cd $OUTPUT_DOCS_DIR
echo "Working directory: ${PWD}"
echo
echo "Removing any previously existing output files from here."

rm -fr *

echo "Creating .nojekyll file."
touch .nojekyll

echo
echo "Changing working directory to ${PUBLIC}."
cd $PUBLIC;
echo "Working directory: ${PWD}"
echo

echo "Copying contents from here to ${OUTPUT_DOCS_DIR}..."

cp -fr * $OUTPUT_DOCS_DIR

echo

echo "Changing working directory back to ${CURRENT_WD}"
cd $CURRENT_WD
echo "Working directory: ${PWD}"

echo "Cleaning up"

echo "Removing and remaking content folder from PREVIOUS Hugo run."
rm -fr $CONTENT
mkdir -p $CONTENT
# Prevent Hugo Docs Builder from recursing into this directory.
touch "${CONTENT}/_SITE_BUILDER_STOP"

echo "Removing and remaking static source folder from PREVIOUS Hugo run."
rm -fr $STATICSOURCE
mkdir -p $STATICSOURCE
# Prevent Hugo Docs Builder from recursing into this directory.
touch "${STATICSOURCE}/_SITE_BUILDER_STOP"

echo "Removing and remaking public folder from PREVIOUS Hugo run."
rm -fr $PUBLIC
mkdir -p $PUBLIC
# Prevent Hugo Docs Builder from recursing into this directory.
touch "${PUBLIC}/_SITE_BUILDER_STOP"


echo
echo "================================================================================="
echo "================================================================================="
echo "================================================================================="
echo
echo "DONE."
echo