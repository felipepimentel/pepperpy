"""Rich text component for console UI"""

from dataclasses import dataclass

from rich.color import Color
from rich.style import Style
from rich.text import Text

from pepperpy.console.ui.components.base import Component, ComponentConfig
from pepperpy.console.ui.styles import StyleConfig, styles


@dataclass
class TextStyle:
    """Text style configuration"""

    color: str | Color | tuple[int, int, int] | None = None
    background: str | Color | tuple[int, int, int] | None = None
    bold: bool = False
    italic: bool = False
    underline: bool = False
    blink: bool = False
    reverse: bool = False
    dim: bool = False


@dataclass
class TextSegment:
    """Text segment with style"""

    text: str
    style: TextStyle | None = None


class RichText(Component):
    """Rich text component"""

    def __init__(self) -> None:
        config = ComponentConfig(
            style={
                "default": StyleConfig(),
                "bold": StyleConfig(bold=True),
                "italic": StyleConfig(italic=True),
                "primary": StyleConfig(color="blue", bold=True),
                "secondary": StyleConfig(color="cyan"),
                "success": StyleConfig(color="green"),
                "warning": StyleConfig(color="yellow"),
                "error": StyleConfig(color="red", bold=True),
            },
        )
        super().__init__(config=config)
        self._segments: list[TextSegment] = []

    def append(self, text: str, style_name: str | None = None) -> None:
        """
        Append text with style

        Args:
            text: Text to append
            style_name: Style name to apply

        """
        style = None
        if style_name:
            style_config = styles.get(style_name)
            style = TextStyle(
                color=style_config.color,
                bold=style_config.bold,
                italic=style_config.italic,
                underline=style_config.underline,
                blink=style_config.blink,
                reverse=style_config.reverse,
                dim=style_config.dim,
            )
        self._segments.append(TextSegment(text=text, style=style))

    def clear(self) -> None:
        """Clear all text"""
        self._segments.clear()

    def render(self) -> Text:
        """
        Render text

        Returns:
            Text: Rendered text

        """
        text = Text()
        for segment in self._segments:
            if segment.style:
                color = segment.style.color
                if isinstance(color, tuple) and len(color) == 3:
                    r, g, b = (float(x) / 255.0 for x in color if isinstance(x, (int, float)))
                    color = Color.from_rgb(r, g, b)

                bgcolor = segment.style.background
                if isinstance(bgcolor, tuple) and len(bgcolor) == 3:
                    r, g, b = (float(x) / 255.0 for x in bgcolor if isinstance(x, (int, float)))
                    bgcolor = Color.from_rgb(r, g, b)

                style = Style(
                    color=color,
                    bgcolor=bgcolor,
                    bold=segment.style.bold,
                    italic=segment.style.italic,
                    underline=segment.style.underline,
                    blink=segment.style.blink,
                    reverse=segment.style.reverse,
                    dim=segment.style.dim,
                )
            else:
                style = styles.apply("default")
            text.append(segment.text, style=style)
        return text
