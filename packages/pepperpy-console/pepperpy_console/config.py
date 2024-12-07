"""Console configuration module."""

from .console_types import ConsoleConfig, LayoutConfig, Theme, ThemeColors

# Default theme configuration
DEFAULT_THEME: Theme = Theme(
    name="default",
    colors=ThemeColors(
        primary="#007acc",
        secondary="#6c757d",
        success="#28a745",
        warning="#ffc107",
        error="#dc3545",
        info="#17a2b8",
        background="#ffffff",
        text="#212529",
    ),
)

# Default layout configuration
DEFAULT_LAYOUT: LayoutConfig = LayoutConfig(
    width=80,
    height=24,
    padding=1,
)

# Default console configuration
DEFAULT_CONFIG: ConsoleConfig = ConsoleConfig(
    theme=DEFAULT_THEME,
    layout=DEFAULT_LAYOUT,
)


class ConsoleManager:
    """Console manager."""

    def __init__(self, config: ConsoleConfig | None = None) -> None:
        """Initialize console manager.

        Args:
            config: Console configuration
        """
        self.config = config or DEFAULT_CONFIG

    def get_theme(self) -> Theme:
        """Get current theme.

        Returns:
            Current theme
        """
        return self.config.theme

    def get_layout(self) -> LayoutConfig:
        """Get current layout.

        Returns:
            Current layout
        """
        return self.config.layout

    def set_theme(self, theme: Theme) -> None:
        """Set theme.

        Args:
            theme: New theme
        """
        self.config.theme = theme

    def set_layout(self, layout: LayoutConfig) -> None:
        """Set layout.

        Args:
            layout: New layout
        """
        self.config.layout = layout
