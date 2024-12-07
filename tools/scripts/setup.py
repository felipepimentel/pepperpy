#!/usr/bin/env python
"""Setup script for development tools."""
import subprocess
from pathlib import Path


def main() -> None:
    """Install development tools dependencies."""
    tools_dir = Path(__file__).parent.parent

    # Instalar dependências das ferramentas
    subprocess.run(
        ["poetry", "install"],
        cwd=tools_dir,
        check=True,
    )


if __name__ == "__main__":
    main()
