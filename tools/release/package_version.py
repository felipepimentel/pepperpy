"""Package version management"""
from dataclasses import dataclass
from pathlib import Path

import toml
from packaging.version import Version


@dataclass
class PackageVersion:
    """Package version information"""
    name: str
    current_version: Version
    new_version: Version | None = None
    
class VersionManager:
    """Manages package versions"""
    
    def __init__(self, packages_dir: Path):
        self.packages_dir = packages_dir
        
    def get_package_version(self, package: Path) -> PackageVersion:
        """Get package version information"""
        pyproject_path = package / "pyproject.toml"
        if not pyproject_path.exists():
            raise FileNotFoundError(f"pyproject.toml not found in {package}")
            
        config = toml.load(pyproject_path)
        version = config["tool"]["poetry"]["version"]
        name = config["tool"]["poetry"]["name"]
        
        return PackageVersion(
            name=name,
            current_version=Version(version)
        )
        
    def update_package_version(self, package: Path, new_version: str) -> None:
        """Update package version"""
        pyproject_path = package / "pyproject.toml"
        config = toml.load(pyproject_path)
        config["tool"]["poetry"]["version"] = new_version
        
        with open(pyproject_path, "w") as f:
            toml.dump(config, f) 