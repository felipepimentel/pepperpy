#!/bin/bash

# Instala as dependências em cada pacote
for package in packages/*; do
  if [ -d "$package" ]; then
    echo "Installing dependencies for $package..."
    cd "$package"
    poetry install
    cd ../..
  fi
done 