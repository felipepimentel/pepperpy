"""Button component implementation"""

from typing import Callable, Optional

from ..keyboard import Key, KeyEvent
from ..styles import Style
from .base import Component, ComponentConfig


class Button(Component):
    """Interactive button component"""

    def __init__(
        self,
        config: ComponentConfig,
        text: str,
        on_click: Optional[Callable[[], None]] = None,
        shortcut: Optional[Key] = None,
        focused_style: Optional[Style] = None,
    ):
        super().__init__(config)
        self.text = text
        self.on_click = on_click
        self.shortcut = shortcut
        self.focused_style = focused_style or Style(bold=True)
        self._focused = False

    @property
    def focused(self) -> bool:
        """Get focus state"""
        return self._focused

    @focused.setter
    def focused(self, value: bool) -> None:
        """Set focus state"""
        self._focused = value

    async def handle_input(self, event: KeyEvent) -> bool:
        """Handle keyboard input"""
        if not self.config.enabled:
            return False

        if self._focused and event.key == Key.ENTER:
            if self.on_click:
                await self.on_click()
            return True

        if self.shortcut and event.key == self.shortcut:
            if self.on_click:
                await self.on_click()
            return True

        return False

    async def _setup(self) -> None:
        """Initialize button"""
        pass

    async def _cleanup(self) -> None:
        """Cleanup button"""
        pass

    async def render(self) -> None:
        """Render button"""
        if not self.config.visible:
            return

        # Apply appropriate style
        style = self.focused_style if self._focused else self.config.style or Style()

        # Move cursor
        print(f"\033[{self.config.y};{self.config.x}H", end="")

        # Calculate button width
        width = self.config.width or len(self.text) + 4

        # Render button
        if self.config.enabled:
            print(f"{style.apply()}[ {self.text:<{width-4}} ]{style.reset()}", end="")
        else:
            print(f"{style.disabled.apply()}[ {self.text:<{width-4}} ]{style.reset()}", end="")

        # Show shortcut if available
        if self.shortcut:
            print(f" ({self.shortcut.value})")
        else:
            print()
