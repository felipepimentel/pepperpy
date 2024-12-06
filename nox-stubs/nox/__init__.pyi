"""Type stubs for nox"""
from collections.abc import Callable
from pathlib import Path
from typing import Any, TypeVar

T = TypeVar('T')

class Session:
    def install(self, *args: str) -> None: ...
    def log(self, msg: str) -> None: ...
    def chdir(self, path: str | Path) -> Any: ...
    def run(self, *args: str, external: bool = False) -> None: ...

class Options:
    sessions: list[str]
    reuse_existing_virtualenvs: bool
    error_on_external_run: bool

options: Options

def session(python: str | list[str]) -> Callable[[T], T]: ... 