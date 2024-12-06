"""Development environment management"""
import subprocess
from pathlib import Path


class DevEnvironment:
    """Manages development environment"""
    
    def __init__(self, root_dir: Path):
        self.root_dir = root_dir
        self.tools_dir = root_dir / "tools"
        self.packages_dir = root_dir / "packages"
        
    def setup(self, python_version: str | None = None) -> None:
        """Setup development environment"""
        # Install pre-commit hooks
        subprocess.run(["pre-commit", "install"], check=True)
        
        # Setup virtual environments
        for package in self.packages_dir.iterdir():
            if package.is_dir():
                self._setup_package(package, python_version)
                
    def _setup_package(self, package: Path, python_version: str | None = None) -> None:
        """Setup single package environment"""
        cmd = ["poetry", "env", "use"]
        if python_version:
            cmd.append(python_version)
            
        subprocess.run(cmd, cwd=package, check=True)
        subprocess.run(["poetry", "install"], cwd=package, check=True) 