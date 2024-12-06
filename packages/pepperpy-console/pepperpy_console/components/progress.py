"""Progress bar component implementation."""

from dataclasses import dataclass, field
from typing import Any

from ..base.component import BaseComponent


@dataclass
class ProgressConfig:
    """Progress bar configuration."""

    total: int = 100
    description: str = ""
    unit: str = "%"
    style: str = "blue"
    metadata: dict[str, Any] = field(default_factory=dict)


class ProgressBar(BaseComponent):
    """Progress bar component."""

    def __init__(self, config: ProgressConfig | None = None) -> None:
        """Initialize progress bar.

        Args:
            config: Progress bar configuration
        """
        super().__init__()
        self.config = config or ProgressConfig()
        self._value: int = 0

    async def initialize(self) -> None:
        """Initialize progress bar."""
        await super().initialize()

    async def render(self) -> Any:
        """Render progress bar."""
        await super().render()
        percentage = min(100, int(self._value / self.config.total * 100))
        return f"{self.config.description} [{percentage}{self.config.unit}]"

    async def cleanup(self) -> None:
        """Cleanup progress bar."""
        await super().cleanup()

    def update(self, value: int) -> None:
        """Update progress value.

        Args:
            value: New progress value
        """
        self._ensure_initialized()
        self._value = min(self.config.total, max(0, value))
