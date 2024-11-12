"""Rich text component implementation"""

import re
from dataclasses import dataclass
from typing import List, Optional

from ..styles import Style
from .base import Component, ComponentConfig


@dataclass
class TextSpan:
    """Styled text span"""

    text: str
    style: Optional[Style] = None


class RichText(Component):
    """Component for displaying styled text"""

    MARKDOWN_PATTERNS = {
        "bold": (r"\*\*(.*?)\*\*", Style(bold=True)),
        "italic": (r"_(.*?)_", Style(italic=True)),
        "code": (r"`(.*?)`", Style(fg_color=(128, 128, 128))),
        "link": (r"\[(.*?)\]\((.*?)\)", Style(underline=True, fg_color=(0, 0, 255))),
    }

    def __init__(
        self,
        config: ComponentConfig,
        text: str,
        parse_markdown: bool = True,
        word_wrap: bool = True,
    ):
        super().__init__(config)
        self.text = text
        self.parse_markdown = parse_markdown
        self.word_wrap = word_wrap
        self._spans: List[TextSpan] = []
        self._wrapped_lines: List[List[TextSpan]] = []

    async def _setup(self) -> None:
        """Initialize rich text"""
        if self.parse_markdown:
            self._spans = self._parse_markdown(self.text)
        else:
            self._spans = [TextSpan(self.text)]

        if self.word_wrap:
            self._wrapped_lines = self._wrap_text()

    async def _cleanup(self) -> None:
        """Cleanup rich text"""
        pass

    def _parse_markdown(self, text: str) -> List[TextSpan]:
        """Parse markdown-style formatting"""
        spans = []
        current_pos = 0

        while current_pos < len(text):
            # Find next markdown pattern
            next_match = None
            next_pattern = None

            for pattern_name, (regex, pattern_style) in self.MARKDOWN_PATTERNS.items():
                match = re.search(regex, text[current_pos:])
                if match and (not next_match or match.start() < next_match.start()):
                    next_match = match
                    next_pattern = (pattern_name, pattern_style)

            if next_match and next_pattern:
                # Add text before pattern
                if next_match.start() > 0:
                    spans.append(TextSpan(text[current_pos : current_pos + next_match.start()]))

                # Add styled text
                pattern_name, pattern_style = next_pattern
                if pattern_name == "link":
                    spans.append(TextSpan(next_match.group(1), pattern_style))
                else:
                    spans.append(TextSpan(next_match.group(1), pattern_style))

                current_pos += next_match.end()
            else:
                # Add remaining text
                spans.append(TextSpan(text[current_pos:]))
                break

        return spans

    def _wrap_text(self) -> List[List[TextSpan]]:
        """Wrap text to component width"""
        if not self.config.width:
            return [self._spans]

        lines = []
        current_line = []
        current_width = 0

        for span in self._spans:
            words = span.text.split()

            for word in words:
                word_width = len(word)

                if current_width + word_width + 1 > self.config.width:
                    if current_line:
                        lines.append(current_line)
                        current_line = []
                        current_width = 0

                if current_line:
                    current_line.append(TextSpan(" ", span.style))
                    current_width += 1

                current_line.append(TextSpan(word, span.style))
                current_width += word_width

        if current_line:
            lines.append(current_line)

        return lines

    async def render(self) -> None:
        """Render rich text"""
        if not self.config.visible:
            return

        y = self.config.y
        base_style = self.config.style or Style()

        if self.word_wrap:
            # Render wrapped lines
            for line in self._wrapped_lines:
                print(f"\033[{y};{self.config.x}H", end="")

                for span in line:
                    style = span.style or base_style
                    print(f"{style.apply()}{span.text}{style.reset()}", end="")

                print()
                y += 1
        else:
            # Render spans in a single line
            print(f"\033[{y};{self.config.x}H", end="")

            for span in self._spans:
                style = span.style or base_style
                print(f"{style.apply()}{span.text}{style.reset()}", end="")
