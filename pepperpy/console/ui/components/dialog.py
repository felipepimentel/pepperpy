"""Dialog component implementation"""

from typing import Callable, List, Optional

from ..styles import Style
from .base import Component, ComponentConfig


class Dialog(Component):
    """Dialog box component"""

    def __init__(
        self,
        config: ComponentConfig,
        title: str,
        content: str,
        buttons: List[str] = None,
        on_close: Optional[Callable[[str], None]] = None,
    ):
        super().__init__(config)
        self.title = title
        self.content = content
        self.buttons = buttons or ["OK"]
        self.on_close = on_close
        self._selected_button = 0
        self._visible = True

    async def _setup(self) -> None:
        """Initialize dialog"""
        pass

    async def _cleanup(self) -> None:
        """Cleanup dialog"""
        pass

    async def render(self) -> None:
        """Render dialog box"""
        if not self._visible:
            return

        style = self.config.style or Style()
        width = self.config.width or max(
            len(self.title) + 4,
            max(len(line) for line in self.content.split("\n")) + 4,
            sum(len(b) + 4 for b in self.buttons) + len(self.buttons) - 1,
        )
        height = self.content.count("\n") + 5

        # Draw box
        print(f"\033[{self.config.y};{self.config.x}H{style.apply()}┌{'─' * (width-2)}┐")

        # Title
        title_pos = (width - len(self.title)) // 2
        print(
            f"\033[{self.config.y+1};{self.config.x}H│{' ' * title_pos}{self.title}{' ' * (width-title_pos-len(self.title)-2)}│"
        )

        print(f"\033[{self.config.y+2};{self.config.x}H├{'─' * (width-2)}┤")

        # Content
        for i, line in enumerate(self.content.split("\n")):
            print(f"\033[{self.config.y+3+i};{self.config.x}H│ {line:<{width-4}} │")

        # Buttons
        button_y = self.config.y + height - 1
        button_x = (
            self.config.x
            + (width - sum(len(b) + 4 for b in self.buttons) - len(self.buttons) + 1) // 2
        )

        for i, button in enumerate(self.buttons):
            if i == self._selected_button:
                print(f"\033[{button_y};{button_x}H[{button}]", end="")
            else:
                print(f"\033[{button_y};{button_x}H {button} ", end="")
            button_x += len(button) + 4

        print(f"{style.reset()}")
