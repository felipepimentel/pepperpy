#!/usr/bin/env python
"""Script to fix deprecated type hints."""

import re
from pathlib import Path

# Mapeamento de tipos deprecados para seus substitutos
TYPE_REPLACEMENTS = {
    r"from typing import ([\w\s,]*?)List([\w\s,]*?)": (
        r"from typing import \1list\2"
    ),
    r"from typing import ([\w\s,]*?)Dict([\w\s,]*?)": (
        r"from typing import \1dict\2"
    ),
    r"from typing import ([\w\s,]*?)Set([\w\s,]*?)": (
        r"from typing import \1set\2"
    ),
    r"from typing import ([\w\s,]*?)Type([\w\s,]*?)": r"from typing import \1type\2",
    r"from typing import ([\w\s,]*?)Tuple([\w\s,]*?)": r"from typing import \1tuple\2",
    r"List\[": r"list[",
    r"Dict\[": r"dict[",
    r"Set\[": r"set[",
    r"Type\[": r"type[",
    r"Tuple\[": r"tuple[",
}

COLLECTIONS_REPLACEMENTS = {
    r"from typing import ([\w\s,]*?)Sequence([\w\s,]*?)": (
        r"from collections.abc import \1Sequence\2"
    ),
    r"from typing import ([\w\s,]*?)AsyncGenerator([\w\s,]*?)": (
        r"from collections.abc import \1AsyncGenerator\2"
    ),
    r"from typing import ([\w\s,]*?)AsyncContextManager([\w\s,]*?)": (
        r"from contextlib import \1AbstractAsyncContextManager\2"
    ),
}

def fix_file(file_path: Path) -> None:
    """Fix type hints in a file."""
    with open(file_path) as f:
        content = f.read()

    # Aplicar substituições
    modified = content
    for pattern, replacement in {**TYPE_REPLACEMENTS, **COLLECTIONS_REPLACEMENTS}.items():
        modified = re.sub(pattern, replacement, modified)

    # Salvar apenas se houver mudanças
    if modified != content:
        print(f"Fixing {file_path}")
        with open(file_path, "w") as f:
            f.write(modified)

def main() -> None:
    """Main function."""
    packages_dir = Path("packages")
    tools_dir = Path("tools")
    
    # Encontrar todos os arquivos Python
    python_files: list[Path] = []
    for directory in [packages_dir, tools_dir]:
        if directory.exists():
            python_files.extend(directory.rglob("*.py"))
            python_files.extend(directory.rglob("*.pyi"))
    
    # Corrigir cada arquivo
    for file_path in python_files:
        fix_file(file_path)

if __name__ == "__main__":
    main() 