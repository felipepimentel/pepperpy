"""Version management utilities"""
from pathlib import Path

import toml


def update_versions(new_version: str) -> None:
    """Update versions in all package pyproject.toml files"""
    packages_dir = Path("packages")
    for package in packages_dir.iterdir():
        if not package.is_dir():
            continue
            
        pyproject_path = package / "pyproject.toml"
        if not pyproject_path.exists():
            continue
            
        config = toml.load(pyproject_path)
        config["tool"]["poetry"]["version"] = new_version
        
        with open(pyproject_path, "w") as f:
            toml.dump(config, f) 