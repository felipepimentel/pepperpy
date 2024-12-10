#!/bin/bash

set -e

BASE_DIR=$(pwd)

for PACKAGE_DIR in packages/*; do
    if git diff --quiet HEAD^ HEAD "$PACKAGE_DIR"; then
        echo "No changes detected in $PACKAGE_DIR, skipping..."
    else
        echo "Changes detected in $PACKAGE_DIR, publishing..."
        poetry build --directory "$PACKAGE_DIR"
        poetry publish --directory "$PACKAGE_DIR" --username $PYPI_USERNAME --password $PYPI_PASSWORD
    fi
done
