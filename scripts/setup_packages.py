"""Script to setup all packages in the correct order."""
import os
import subprocess
from pathlib import Path


def setup_package(package_path: Path) -> None:
    """Setup a single package.
    
    Args:
        package_path: Path to the package directory
    """
    print(f"Setting up {package_path.name}...")
    
    # First update the lock file
    subprocess.run(
        ["poetry", "lock", "--no-update"],
        cwd=package_path,
        check=True,
    )
    
    # Then install dependencies
    subprocess.run(
        ["poetry", "install"],
        cwd=package_path,
        check=True,
    )


def main() -> None:
    """Main function."""
    # Get the root directory
    root = Path(__file__).parent.parent
    
    # Setup core package first
    core_path = root / "packages" / "pepperpy-core"
    setup_package(core_path)
    
    # Setup other packages
    packages_dir = root / "packages"
    for package_dir in packages_dir.iterdir():
        if package_dir.is_dir() and package_dir != core_path:
            setup_package(package_dir)


if __name__ == "__main__":
    main() 