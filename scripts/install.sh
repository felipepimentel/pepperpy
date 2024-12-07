#!/bin/bash

# Função para instalar um pacote
install_package() {
    local package=$1
    echo "Installing dependencies for $package..."
    cd "$package" || exit
    
    # Limpa qualquer ambiente virtual existente
    poetry env remove --all
    
    # Instala as dependências
    poetry install --no-root
    
    cd - || exit
}

# Instala primeiro o pepperpy-core
echo "Installing core package first..."
install_package "packages/pepperpy-core"

# Instala os outros pacotes
for package in packages/*; do
    if [ -d "$package" ] && [ "$(basename "$package")" != "pepperpy-core" ]; then
        install_package "$package"
    fi
done 