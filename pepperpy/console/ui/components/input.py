"""Input component implementations"""

from typing import Callable, Optional

from .base import Component, ComponentConfig


class TextInput(Component):
    """Text input component"""

    def __init__(
        self,
        config: ComponentConfig,
        placeholder: str = "",
        on_change: Optional[Callable[[str], None]] = None,
        on_submit: Optional[Callable[[str], None]] = None,
    ):
        super().__init__(config)
        self.placeholder = placeholder
        self.on_change = on_change
        self.on_submit = on_submit
        self._value = ""
        self._focused = False

    @property
    def value(self) -> str:
        """Get current input value"""
        return self._value

    @value.setter
    def value(self, new_value: str) -> None:
        """Set input value"""
        if new_value != self._value:
            self._value = new_value
            if self.on_change:
                self.on_change(new_value)

    async def _setup(self) -> None:
        """Initialize input"""
        pass

    async def _cleanup(self) -> None:
        """Cleanup input"""
        pass

    async def render(self) -> None:
        """Render input component"""
        if not self.config.visible:
            return

        # Move cursor to component position
        print(f"\033[{self.config.y};{self.config.x}H", end="")

        # Render input box
        width = self.config.width or len(self.placeholder) + 4
        content = self._value or self.placeholder

        if len(content) > width - 4:
            content = content[: width - 7] + "..."

        # Apply style if focused
        if self._focused and self.config.style:
            print(f"{self.config.style.apply()}[ {content:<{width-4}} ]{self.config.style.reset()}")
        else:
            print(f"[ {content:<{width-4}} ]")
