"""Form component implementation"""

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional

from ..keyboard import Key, KeyEvent
from ..styles import Style
from .base import Component, ComponentConfig
from .button import Button
from .input import TextInput


@dataclass
class FormField:
    """Form field definition"""

    name: str
    label: str
    type: str = "text"
    required: bool = True
    validator: Optional[Callable[[str], bool]] = None
    initial: Any = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class Form(Component):
    """Form component for data input"""

    def __init__(
        self,
        config: ComponentConfig,
        fields: List[FormField],
        on_submit: Optional[Callable[[Dict[str, Any]], None]] = None,
        show_validation: bool = True,
    ):
        super().__init__(config)
        self.fields = fields
        self.on_submit = on_submit
        self.show_validation = show_validation
        self._inputs: Dict[str, TextInput] = {}
        self._submit_button: Optional[Button] = None
        self._current_field = 0
        self._errors: Dict[str, str] = {}

    async def _setup(self) -> None:
        """Initialize form components"""
        y = self.config.y

        # Create input fields
        for form_field in self.fields:
            input_config = ComponentConfig(
                x=self.config.x + len(form_field.label) + 2,
                y=y,
                width=self.config.width - len(form_field.label) - 4 if self.config.width else None,
                style=self.config.style,
            )

            self._inputs[form_field.name] = TextInput(
                config=input_config, placeholder=form_field.label, initial_value=form_field.initial
            )
            y += 2

        # Create submit button
        button_config = ComponentConfig(x=self.config.x, y=y + 1, style=self.config.style)

        self._submit_button = Button(
            config=button_config, text="Submit", on_click=self._handle_submit
        )

        # Initialize all components
        for input_field in self._inputs.values():
            await input_field.initialize()
        await self._submit_button.initialize()

    async def _cleanup(self) -> None:
        """Cleanup form components"""
        for input_field in self._inputs.values():
            await input_field.cleanup()
        if self._submit_button:
            await self._submit_button.cleanup()

    async def _handle_submit(self) -> None:
        """Handle form submission"""
        self._errors.clear()

        # Validate all fields
        values = {}
        for form_field in self.fields:
            value = self._inputs[form_field.name].value

            if form_field.required and not value:
                self._errors[form_field.name] = "This field is required"
                continue

            if form_field.validator and value:
                try:
                    if not form_field.validator(value):
                        self._errors[form_field.name] = "Invalid value"
                        continue
                except Exception as e:
                    self._errors[form_field.name] = str(e)
                    continue

            values[form_field.name] = value

        # If no errors and callback provided, submit
        if not self._errors and self.on_submit:
            await self.on_submit(values)

    async def handle_input(self, event: KeyEvent) -> bool:
        """Handle keyboard input"""
        if event.key == Key.TAB:
            # Move to next field
            self._current_field = (self._current_field + 1) % (len(self.fields) + 1)
            return True

        # Delegate to current component
        if self._current_field < len(self.fields):
            current_field = self.fields[self._current_field]
            return await self._inputs[current_field.name].handle_input(event)
        else:
            return await self._submit_button.handle_input(event)

    async def render(self) -> None:
        """Render form"""
        if not self.config.visible:
            return

        # Render fields
        for i, form_field in enumerate(self.fields):
            # Render label
            print(f"\033[{self.config.y + i*2};{self.config.x}H{form_field.label}:", end="")

            # Render input
            input_field = self._inputs[form_field.name]
            input_field.focused = i == self._current_field
            await input_field.render()

            # Render error if any
            if self.show_validation and form_field.name in self._errors:
                error_style = Style(fg_color=(255, 0, 0))
                print(
                    f"\033[{self.config.y + i*2 + 1};{self.config.x}H{error_style.apply()}"
                    f"{self._errors[form_field.name]}{error_style.reset()}"
                )

        # Render submit button
        if self._submit_button:
            self._submit_button.focused = self._current_field == len(self.fields)
            await self._submit_button.render()
