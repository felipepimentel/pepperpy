"""Console configuration."""

from dataclasses import dataclass

from .types import ConsoleConfig, LayoutConfig, Theme, ThemeColors

DEFAULT_THEME = Theme(
    name="default",
    colors=ThemeColors(
        primary="#00ff00",
        secondary="#0000ff",
        accent="#ff0000",
        background="#000000",
        foreground="#ffffff",
    ),
)

DEFAULT_LAYOUT = LayoutConfig(
    width=80,
    height=24,
)

DEFAULT_CONFIG = ConsoleConfig(
    theme=DEFAULT_THEME,
    layout=DEFAULT_LAYOUT,
)


@dataclass
class ConfigManager:
    """Configuration manager."""

    def __init__(self, config: ConsoleConfig | None = None) -> None:
        """Initialize configuration manager.

        Args:
            config: Console configuration
        """
        self.config = config or DEFAULT_CONFIG
        self._initialized = False

    @property
    def is_initialized(self) -> bool:
        """Check if manager is initialized."""
        return self._initialized

    async def initialize(self) -> None:
        """Initialize manager."""
        if not self._initialized:
            await self._setup()
            self._initialized = True

    async def cleanup(self) -> None:
        """Cleanup manager resources."""
        if self._initialized:
            await self._teardown()
            self._initialized = False

    def _ensure_initialized(self) -> None:
        """Ensure manager is initialized."""
        if not self._initialized:
            raise RuntimeError("Manager not initialized")

    async def _setup(self) -> None:
        """Setup manager resources."""
        pass

    async def _teardown(self) -> None:
        """Teardown manager resources."""
        pass

    def get_theme(self) -> Theme:
        """Get current theme."""
        self._ensure_initialized()
        return self.config.theme

    def get_layout(self) -> LayoutConfig:
        """Get current layout."""
        self._ensure_initialized()
        return self.config.layout

    def update_theme(self, theme: Theme) -> None:
        """Update theme.

        Args:
            theme: New theme

        Raises:
            RuntimeError: If manager not initialized
        """
        self._ensure_initialized()
        self.config.theme = theme

    def update_layout(self, layout: LayoutConfig) -> None:
        """Update layout.

        Args:
            layout: New layout

        Raises:
            RuntimeError: If manager not initialized
        """
        self._ensure_initialized()
        self.config.layout = layout
