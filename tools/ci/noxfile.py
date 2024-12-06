"""Nox configuration file for running tests and checks."""

from pathlib import Path

import nox
from nox.sessions import Session

# Configurações do nox
nox.needs_version = ">=2024.0.0"
nox.options.sessions = ["lint", "typecheck", "test"]
nox.options.reuse_existing_virtualenvs = True

# Diretórios a serem verificados
PACKAGE_DIRS = [
    "packages/pepperpy-core",
    "packages/pepperpy-console",
    "packages/pepperpy-db",
    "packages/pepperpy-files",
]


@nox.session(python="3.12")
def lint(session: Session) -> None:
    """Run linting checks."""
    session.install("ruff", "black")
    session.run("ruff", "check", ".")
    session.run("black", "--check", ".")


@nox.session(python="3.12")
def typecheck(session: Session) -> None:
    """Run type checking."""
    session.install("mypy")
    for package in PACKAGE_DIRS:
        session.run("mypy", package)


@nox.session(python="3.12")
def test(session: Session) -> None:
    """Run tests."""
    session.install("pytest", "pytest-asyncio", "pytest-cov")
    for package in PACKAGE_DIRS:
        if (Path(package) / "tests").exists():
            session.run("pytest", f"{package}/tests")


@nox.session(python="3.12")
def coverage(session: Session) -> None:
    """Run coverage checks."""
    session.install("coverage[toml]", "pytest", "pytest-cov")
    session.run(
        "pytest",
        "--cov=pepperpy",
        "--cov-report=term-missing",
        "--cov-report=xml",
        *PACKAGE_DIRS,
    )
