import subprocess
import sys


def lint() -> None:
    """Run all linters: Ruff, Black, and isort."""
    commands = [
        ["ruff", "check", ".", "--fix"],
        ["black", "."],
        ["isort", "."],
    ]

    for command in commands:
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Command '{' '.join(command)}' failed with exit code {e.returncode}")
            sys.exit(e.returncode)


if __name__ == "__main__":
    lint()
