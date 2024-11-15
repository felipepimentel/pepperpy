"""Form components for console UI"""

from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from rich.style import Style
from rich.text import Text

from pepperpy.console.ui.components.base import Component, ComponentConfig
from pepperpy.console.ui.keyboard import (
    BACKSPACE,
    ENTER,
    LEFT,
    RIGHT,
    TAB,
    Key,
    KeyCode,
)
from pepperpy.console.ui.styles import styles


@dataclass
class FormField:
    """Form field configuration"""

    name: str
    label: str
    value: str = ""
    required: bool = True
    validators: list[Callable[[str], bool]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


class FormComponent(Component, ABC):
    """Base class for form components"""

    def __init__(self) -> None:
        super().__init__(
            config=ComponentConfig(
                style={
                    "default": Style(color="white"),
                    "focused": Style(color="cyan", bold=True),
                    "disabled": Style(color="gray50", dim=True),
                },
            ),
        )
        self.focused: bool = False

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize component"""

    @abstractmethod
    async def cleanup(self) -> None:
        """Cleanup component"""

    @abstractmethod
    async def handle_input(self, key: Key) -> bool:
        """
        Handle input event

        Args:
            key: Input key

        Returns:
            bool: True if input was handled

        """

    @abstractmethod
    def render(self) -> Text:
        """
        Render component

        Returns:
            Text: Rendered component

        """


class Form(Component):
    """Form component"""

    def __init__(self) -> None:
        super().__init__(
            config=ComponentConfig(
                style={
                    "default": Style(color="white"),
                    "focused": Style(color="cyan", bold=True),
                    "disabled": Style(color="gray50", dim=True),
                },
            ),
        )
        self.components: list[FormComponent] = []
        self.focused_index = 0

    def add_field(self, field: FormField) -> None:
        """Add field to form"""
        self.components.append(TextInput(field))

    def add_button(self, label: str, callback: Callable[[], None]) -> None:
        """Add button to form"""
        self.components.append(Button(label, callback))

    async def initialize(self) -> None:
        """Initialize form"""
        for component in self.components:
            await component.initialize()
        if self.components:
            self.components[0].focused = True

    async def cleanup(self) -> None:
        """Cleanup form"""
        for component in self.components:
            await component.cleanup()

    async def handle_input(self, key: Key) -> bool:
        """Handle input event"""
        if key == TAB:
            self._focus_next()
            return True

        current = self.components[self.focused_index]
        return await current.handle_input(key)

    def _focus_next(self) -> None:
        """Focus next component"""
        if not self.components:
            return

        self.components[self.focused_index].focused = False
        self.focused_index = (self.focused_index + 1) % len(self.components)
        self.components[self.focused_index].focused = True

    def render(self) -> Text:
        """Render form"""
        text = Text()
        for i, component in enumerate(self.components):
            if i > 0:
                text.append("\n")
            text.append(component.render())
        return text


class TextInput(FormComponent):
    """Text input component"""

    def __init__(self, field: FormField) -> None:
        super().__init__()
        self.field = field
        self.value = field.value
        self.cursor_pos = len(self.value)

    async def initialize(self) -> None:
        """Initialize component"""

    async def cleanup(self) -> None:
        """Cleanup component"""

    async def handle_input(self, key: Key) -> bool:
        """Handle input event"""
        if not self.focused:
            return False

        if key == BACKSPACE and self.cursor_pos > 0:
            self.value = (
                self.value[: self.cursor_pos - 1] + self.value[self.cursor_pos :]
            )
            self.cursor_pos -= 1
            return True

        if key == LEFT and self.cursor_pos > 0:
            self.cursor_pos -= 1
            return True

        if key == RIGHT and self.cursor_pos < len(self.value):
            self.cursor_pos += 1
            return True

        # Verificar se é uma tecla de caractere
        if isinstance(key.code, str) or (
            isinstance(key.code, KeyCode) and len(str(key.code)) == 1
        ):
            char = str(key.code)
            self.value = (
                self.value[: self.cursor_pos] + char + self.value[self.cursor_pos :]
            )
            self.cursor_pos += 1
            return True

        return False

    def render(self) -> Text:
        """Render text input"""
        text = Text()
        text.append(f"{self.field.label}: ", style=styles.apply("default"))

        # Render input value with cursor
        if self.focused:
            style = styles.apply("focused")
            if self.cursor_pos < len(self.value):
                text.append(
                    self.value[: self.cursor_pos] + "█" + self.value[self.cursor_pos :],
                    style=style,
                )
            else:
                text.append(self.value + "█", style=style)
        else:
            text.append(self.value, style=styles.apply("default"))

        return text


class Button(FormComponent):
    """Button component"""

    def __init__(self, label: str, callback: Callable[[], None]) -> None:
        super().__init__()
        self.label = label
        self.callback = callback

    async def initialize(self) -> None:
        """Initialize component"""

    async def cleanup(self) -> None:
        """Cleanup component"""

    async def handle_input(self, key: Key) -> bool:
        """Handle input event"""
        if not self.focused:
            return False

        if key == ENTER:
            self.callback()
            return True

        return False

    def render(self) -> Text:
        """Render button"""
        style = styles.apply("focused" if self.focused else "default")
        return Text(f"[ {self.label} ]", style=style)
