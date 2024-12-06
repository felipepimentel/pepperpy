"""Development environment setup utilities."""

import os
import shutil
import subprocess
import venv
from pathlib import Path
from typing import Any

# Type aliases
InstalledPackages = dict[str, Path]
Dependencies = list[str]


def _get_packages() -> list[str]:
    """Get all package names from packages directory."""
    packages_dir = Path("packages")
    return [
        p.name
        for p in packages_dir.iterdir()
        if p.is_dir() and (p / "pyproject.toml").exists()
    ]


def venv_exists() -> bool:
    """Check if virtual environment exists."""
    venv_path = Path(".venv")
    return venv_path.exists() and (venv_path / "pyvenv.cfg").exists()


def _validate_executable(path: str) -> str:
    """Validate executable path."""
    exe_path = shutil.which(path)
    if not exe_path:
        raise ValueError(f"Executable not found: {path}")
    return str(Path(exe_path).resolve())


def _run_command(cmd: list[str], **kwargs: Any) -> None:
    """Run a command safely.

    Args:
        cmd: Command and arguments to run
        kwargs: Additional arguments for subprocess.run
    """
    try:
        subprocess.run(cmd, check=True, **kwargs)
    except subprocess.CalledProcessError as e:
        print(f"Error running command {' '.join(cmd)}: {e}")
        raise


def create_venv() -> None:
    """Create virtual environment."""
    print("Creating virtual environment...")
    venv.create(".venv", with_pip=True)

    # Validate and use resolved paths
    pip_path = ".venv/bin/pip" if os.name != "nt" else ".venv\\Scripts\\pip"
    pip_exe = str(Path(pip_path).resolve())
    if not Path(pip_exe).exists():
        raise ValueError(f"Pip not found at: {pip_exe}")

    _run_command([pip_exe, "install", "--upgrade", "pip"])
    _run_command([pip_exe, "install", "poetry"])


def update_lock_file(package_path: str) -> None:
    """Update poetry.lock file."""
    print(f"Updating lock file for {package_path}...")
    poetry_exe = _validate_executable("poetry")
    _run_command([poetry_exe, "lock", "--no-update"], cwd=package_path)


def install_package(package_path: str) -> None:
    """Install package using poetry."""
    print(f"Installing {package_path}...")
    update_lock_file(package_path)
    poetry_exe = _validate_executable("poetry")
    _run_command([poetry_exe, "install"], cwd=package_path)


def install_dev_tools() -> None:
    """Install development tools."""
    print("Installing development tools...")
    tools = [
        "pytest",
        "pytest-asyncio",
        "pytest-cov",
        "black",
        "ruff",
        "mypy",
        "pre-commit",
    ]
    poetry_exe = _validate_executable("poetry")
    _run_command([poetry_exe, "add", "--group", "dev", *tools])


def setup_dev_environment() -> None:
    """Setup development environment."""
    if not venv_exists():
        create_venv()

    print("Setting up monorepo...")
    update_lock_file(".")
    poetry_exe = _validate_executable("poetry")
    _run_command([poetry_exe, "install"])

    # Automatically detect and install all packages
    packages = _get_packages()
    print(f"Found packages: {', '.join(packages)}")

    for package in packages:
        install_package(f"packages/{package}")

    install_dev_tools()
    print("\nDevelopment environment setup complete!")


if __name__ == "__main__":
    setup_dev_environment()
