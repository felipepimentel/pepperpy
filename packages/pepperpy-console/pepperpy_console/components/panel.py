"""Panel component implementation."""

from dataclasses import dataclass, field
from typing import Any, Literal

from ..base.component import BaseComponent


@dataclass
class PanelConfig:
    """Panel configuration."""

    title: str = ""
    border_style: Literal["single", "double", "rounded", "none"] = "single"
    padding: tuple[int, int] = (1, 1)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate configuration."""
        valid_styles = ["single", "double", "rounded", "none"]
        if self.border_style not in valid_styles:
            raise ValueError(
                f"Invalid border style: {self.border_style}. "
                f"Must be one of: {', '.join(valid_styles)}"
            )


class Panel(BaseComponent):
    """Panel component."""

    def __init__(self, config: PanelConfig | None = None) -> None:
        """Initialize panel."""
        super().__init__()
        self.config = config or PanelConfig()
        self._initialized = False

    @property
    def is_initialized(self) -> bool:
        """Check if panel is initialized."""
        return self._initialized

    async def initialize(self) -> None:
        """Initialize panel."""
        await super().initialize()
        self._initialized = True

    async def render(self) -> Any:
        """Render panel."""
        await super().render()
        # TODO: Implement actual rendering with rich.Panel
        return {
            "title": self.config.title,
            "border_style": self.config.border_style,
            "padding": self.config.padding,
        }

    async def cleanup(self) -> None:
        """Cleanup panel."""
        await super().cleanup()
        self._initialized = False
