#!/usr/bin/env python
"""Script to fix exception imports."""

import re
from pathlib import Path

REPLACEMENTS = {
    r"from .*?exceptions import PepperpyError": "from pepperpy_core.exceptions import PepperpyError",
    r"from \.\.exceptions import PepperpyError": "from ..exceptions import PepperpyError",
    r"from \.exceptions import PepperpyError": "from .exceptions import PepperpyError",
    r"from pepperpy_core\.exceptions import PepperpyError": "from pepperpy_core.exceptions import PepperpyError",
    r"class \w+Error\(PepperpyError\)": lambda m: m.group(0).replace("PepperpyError", "PepperpyError"),
    r"PepperpyError": "PepperpyError",
}


def fix_file(file_path: Path) -> None:
    """Fix imports in a file."""
    try:
        content = file_path.read_text()
        modified = content

        for pattern, replacement in REPLACEMENTS.items():
            if callable(replacement):
                modified = re.sub(pattern, replacement, modified)
            else:
                modified = re.sub(pattern, replacement, modified)

        if modified != content:
            print(f"Fixing {file_path}")
            file_path.write_text(modified)
    except Exception as e:
        print(f"Error processing {file_path}: {e}")


def main() -> None:
    """Main function."""
    # Procurar em todos os pacotes
    packages_dir = Path("packages")
    python_files: list[Path] = []
    
    # Coletar todos os arquivos Python de todos os pacotes
    for package_dir in packages_dir.iterdir():
        if package_dir.is_dir():
            python_files.extend(package_dir.rglob("*.py"))
    
    # Processar cada arquivo
    for file_path in python_files:
        fix_file(file_path)


if __name__ == "__main__":
    main() 