"""Virtual environment management utilities"""
import subprocess
from pathlib import Path


class VenvManager:
    """Manages virtual environments for packages"""
    
    def __init__(self, packages_dir: Path):
        self.packages_dir = packages_dir
        
    def create_venv(self, package: Path, python_version: str | None = None) -> None:
        """Create virtual environment for package"""
        try:
            cmd = ["poetry", "env", "use"]
            if python_version:
                cmd.append(python_version)
                
            subprocess.run(cmd, cwd=package, check=True)
            subprocess.run(["poetry", "install"], cwd=package, check=True)
            
        except subprocess.CalledProcessError as e:
            print(f"Failed to create venv for {package.name}: {e}")
            
    def cleanup_venv(self, package: Path) -> None:
        """Remove virtual environment"""
        venv_dir = package / ".venv"
        if venv_dir.exists():
            subprocess.run(["rm", "-rf", str(venv_dir)], check=True)
            
    def sync_venv(self, package: Path) -> None:
        """Sync virtual environment with dependencies"""
        subprocess.run(["poetry", "install", "--sync"], cwd=package, check=True) 