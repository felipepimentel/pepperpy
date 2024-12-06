"""Rich library stubs."""
from typing import Any, TextIO

class Console:
    """Rich console stub."""
    def __init__(
        self,
        *,
        stderr: bool = False,
        file: TextIO | None = None,
        force_terminal: bool | None = None,
        color_system: str | None = "auto",
        record: bool = False,
        markup: bool = True,
        emoji: bool = True,
        highlight: bool = True,
        width: int | None = None,
        height: int | None = None,
    ) -> None: ...

    @property
    def width(self) -> int: ...

    @property
    def height(self) -> int: ...

    def print(self, *args: Any, **kwargs: Any) -> None: ... 