#!/usr/bin/env python
"""Script to fix imports in the project."""
import re
from pathlib import Path

REPLACEMENTS = {
    r"from .*?exceptions import FileSystemError": "from pepperpy_files.exceptions import FileError",
    r"from \.\.exceptions import FileSystemError": "from ..exceptions import FileError",
    r"FileSystemError": "FileError",
}

def fix_file(file_path: Path) -> None:
    """Fix imports in a file."""
    content = file_path.read_text()
    modified = content

    for pattern, replacement in REPLACEMENTS.items():
        modified = re.sub(pattern, replacement, modified)

    if modified != content:
        print(f"Fixing {file_path}")
        file_path.write_text(modified)

def main() -> None:
    """Main function."""
    root = Path("packages/pepperpy-files")
    python_files = list(root.rglob("*.py"))
    
    for file_path in python_files:
        fix_file(file_path)

if __name__ == "__main__":
    main() 