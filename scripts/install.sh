#!/bin/bash
set -e

# Install core package first
echo "Installing pepperpy-core..."
cd packages/pepperpy-core
poetry env remove --all
poetry install --no-interaction --no-root
cd ../..

# Install other packages
for dir in packages/*; do
    if [ -d "$dir" ] && [ "$(basename $dir)" != "pepperpy-core" ]; then
        echo "Installing $(basename $dir)..."
        cd "$dir"
        poetry env remove --all
        poetry install --no-interaction --no-root
        cd ../..
    fi
done 