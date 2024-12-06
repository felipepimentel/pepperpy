"""Type stubs for rich.console."""

from typing import Any, TextIO

class Console:
    """Rich console stub."""

    width: int
    height: int

    def __init__(
        self,
        *,
        stderr: bool = False,
        file: TextIO | None = None,
        force_terminal: bool | None = None,
        color_system: str | None = None,
        record: bool = False,
        markup: bool = True,
        emoji: bool = True,
        highlight: bool = True,
        width: int | None = None,
        height: int | None = None,
    ) -> None: ...
    def print(self, *args: Any, **kwargs: Any) -> None: ...
    def clear(self) -> None: ...
