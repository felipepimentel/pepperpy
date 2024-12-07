"""Type stubs for nox."""

from collections.abc import Callable
from typing import TypeVar, overload

T = TypeVar("T")

class Options:
    """Nox options configuration."""

    sessions: list[str]
    reuse_existing_virtualenvs: bool
    error_on_external_run: bool
    force_venv_backend: str | None

# Module level attributes
needs_version: str
options: Options

@overload
def session(*, python: str | list[str], venv_backend: str | None = None) -> Callable[[T], T]: ...
@overload
def session(func: T) -> T: ...
