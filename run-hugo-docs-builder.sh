#!/bin/bash

# ARG_1 is the source content directory

echo

if [ $# -ne 2 ];
    then
        echo "Aborting."
        echo "    There should be exactly two argument, the source content directory and the output docs directory."
        echo "Usage:"
        echo "    bash run-hugo-docs-builder.sh CONTENT_DIR OUTPUT_DOCS_DIR."
        exit 1
fi

CONTENT_DIR="$(cd "$(dirname "${1}")"; pwd)/$(basename "${1}")";
OUTPUT_DOCS_DIR="$(cd "$(dirname "${2}")"; pwd)/$(basename "${2}")";

echo "================================================================================="
echo "================================================================================="
echo "================================================================================="
echo
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
echo "This script lives in ${SCRIPT_DIR}.";
echo
echo "Using source content directory: ${CONTENT_DIR}.";
echo "Using output docs directory: ${OUTPUT_DOCS_DIR}.";
echo
echo "Running ${SCRIPT_DIR}/hugo_docs_builder.py ${CONTENT_DIR}..."

python "${SCRIPT_DIR}/hugo_docs_builder.py" $CONTENT_DIR

if [ $? -ne 0 ]; then
    echo
    echo "Aborting."
    echo "hugo_docs_builder.py failed."
    echo "See output for details."
    exit 1
fi

CURRENT_WD=$PWD;

echo "Removing public folder from PREVIOUS Hugo run."
rm -fr "${SCRIPT_DIR}/site-hugo-template/public"

echo
echo "Current working directory: ${CURRENT_WD}".
echo "Changing working directory to ${SCRIPT_DIR}/site-hugo-template."
cd "${SCRIPT_DIR}/site-hugo-template"
echo "Working directory: ${PWD}"
echo

echo "Running hugo -D"

hugo -D

echo
mkdir -p "${SCRIPT_DIR}/site-hugo-template/content"
echo "Changing working directory to ${SCRIPT_DIR}/site-hugo-template/content."
cd "${SCRIPT_DIR}/site-hugo-template/content"
echo "Working directory: ${PWD}"
echo
echo "Removing the (temporary) files from here."

rm -fr *

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
echo "Changing working directory to ${SCRIPT_DIR}/site-hugo-template/public."
cd "${SCRIPT_DIR}/site-hugo-template/public"
echo "Working directory: ${PWD}"
echo

echo "Copying contents from here to ${OUTPUT_DOCS_DIR}..."

cp -fr * $OUTPUT_DOCS_DIR

echo

echo "Changing working directory back to ${CURRENT_WD}"
cd $CURRENT_WD
echo "Working directory: ${PWD}"

echo
echo "Removing public folder from THIS Hugo run."
rm -fr "${SCRIPT_DIR}/site-hugo-template/public"

echo
echo "================================================================================="
echo "================================================================================="
echo "================================================================================="
echo
echo "DONE."
echo