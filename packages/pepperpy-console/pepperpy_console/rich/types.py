"""Rich console type definitions."""

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class RichConsoleProtocol(Protocol):
    """Protocol for Rich console interface."""

    def print(self, *args: Any, **kwargs: Any) -> None:
        """Print to console."""
        ...

    def clear(self) -> None:
        """Clear console."""
        ...

    @property
    def width(self) -> int:
        """Get console width."""
        ...

    @property
    def height(self) -> int:
        """Get console height."""
        ...
