"""Test runner utilities"""
import subprocess
from collections.abc import Sequence
from pathlib import Path


class TestRunner:
    """Manages test execution"""
    
    def __init__(self, packages_dir: Path):
        self.packages_dir = packages_dir
        
    def run_tests(
        self,
        packages: Sequence[str] | None = None,
        markers: Sequence[str] | None = None,
        coverage: bool = True
    ) -> None:
        """Run tests for specified packages"""
        packages = packages or [p.name for p in self.packages_dir.iterdir() if p.is_dir()]
        
        for package in packages:
            cmd = ["pytest"]
            if coverage:
                cmd.extend(["--cov", "--cov-report=term-missing"])
            if markers:
                cmd.extend(["-m", " or ".join(markers)])
                
            try:
                subprocess.run(cmd, cwd=self.packages_dir / package, check=True)
            except subprocess.CalledProcessError as e:
                print(f"Tests failed for {package}: {e}") 