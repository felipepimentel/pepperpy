"""Debugger utilities."""

import inspect
from dataclasses import dataclass, field
from typing import Any

from ..logging import BaseLogger
from ..types import JsonDict


@dataclass
class DebugInfo:
    """Debug information."""

    name: str
    module: str
    function: str
    line: int
    message: str
    metadata: JsonDict = field(default_factory=dict)


class Debugger:
    """Debug utility."""

    def __init__(
        self,
        name: str,
        logger: BaseLogger | None = None,
        metadata: JsonDict | None = None,
    ) -> None:
        """Initialize debugger.

        Args:
            name: Debugger name
            logger: Optional logger
            metadata: Optional metadata
        """
        self.name = name
        self.logger = logger
        self.metadata = metadata or {}

    def get_caller_info(self, depth: int = 1) -> dict[str, Any]:
        """Get caller information.

        Args:
            depth: Call stack depth

        Returns:
            Caller information
        """
        frame = inspect.currentframe()
        try:
            for _ in range(depth + 1):
                if not frame:
                    break
                frame = frame.f_back

            if not frame:
                return {}

            info = inspect.getframeinfo(frame)
            return {
                "module": info.filename,
                "function": info.function,
                "line": info.lineno,
            }
        finally:
            del frame

    def debug(
        self,
        message: str,
        depth: int = 1,
        metadata: JsonDict | None = None,
    ) -> None:
        """Log debug message.

        Args:
            message: Debug message
            depth: Call stack depth
            metadata: Optional metadata
        """
        info = self.get_caller_info(depth)
        debug_info = DebugInfo(
            name=self.name,
            module=info.get("module", "unknown"),
            function=info.get("function", "unknown"),
            line=info.get("line", 0),
            message=message,
            metadata={**self.metadata, **(metadata or {})},
        )

        if self.logger:
            self.logger.debug(
                f"{debug_info.module}:{debug_info.function}:{debug_info.line} - {message}",
                debug=debug_info.__dict__,
            )
