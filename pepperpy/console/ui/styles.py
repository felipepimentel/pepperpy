"""UI style definitions"""

from dataclasses import dataclass

from rich.color import Color
from rich.style import Style


@dataclass
class StyleConfig:
    """Style configuration"""

    color: str | Color | tuple[int, int, int] | None = None
    bold: bool = False
    italic: bool = False
    underline: bool = False
    blink: bool = False
    reverse: bool = False
    dim: bool = False

    def to_rich_style(self) -> Style:
        """Convert to Rich Style"""
        # Converter tuple de cores para Color se necessário
        color = self.color
        if isinstance(color, tuple) and len(color) == 3:
            # Ensure that the values are integers between 0 and 255
            r, g, b = (float(x) / 255.0 for x in color if isinstance(x, int) and 0 <= x <= 255)
            color = Color.from_rgb(r, g, b)

        return Style(
            color=color,
            bold=self.bold,
            italic=self.italic,
            underline=self.underline,
            blink=self.blink,
            reverse=self.reverse,
            dim=self.dim,
        )


class StyleManager:
    """Style manager for UI components"""

    def __init__(self):
        self._styles: dict[str, StyleConfig] = {}

    def register(self, name: str, style: StyleConfig) -> None:
        """Register style"""
        self._styles[name] = style

    def get(self, name: str, default: StyleConfig | None = None) -> StyleConfig:
        """Get style by name"""
        return self._styles.get(name, default or StyleConfig())

    def apply(self, name: str) -> Style:
        """Get Rich Style by name"""
        return self.get(name).to_rich_style()


# Global style manager instance
styles = StyleManager()

# Register default styles
styles.register("default", StyleConfig())
styles.register("primary", StyleConfig(color="blue", bold=True))
styles.register("secondary", StyleConfig(color="cyan"))
styles.register("success", StyleConfig(color="green"))
styles.register("warning", StyleConfig(color="yellow"))
styles.register("error", StyleConfig(color="red", bold=True))
styles.register("info", StyleConfig(color="white"))
styles.register("muted", StyleConfig(dim=True))
