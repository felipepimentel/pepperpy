from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.message import Message
from textual.validation import Validator
from textual.widgets import Button, Checkbox, Input, Label, Select, Static, TextArea


@dataclass
class FormField:
    """Form field configuration"""

    name: str
    label: str
    type: str = "text"
    required: bool = False
    validators: List[Validator] = field(default_factory=list)
    default: Any = None
    help_text: Optional[str] = None
    choices: Optional[List[str]] = None
    placeholder: Optional[str] = None
    disabled: bool = False


class TUIForm(Vertical):
    """Rich TUI form widget"""

    # Define CSS como uma propriedade de classe
    CSS_PATH = "tui_form.css"  # Movido o CSS para um arquivo separado

    class Submitted(Message):
        """Form submitted message"""

        def __init__(self, values: Dict[str, Any]) -> None:
            self.values = values
            super().__init__()

    class Validated(Message):
        """Form validation message"""

        def __init__(self, valid: bool, errors: Dict[str, str]) -> None:
            self.valid = valid
            self.errors = errors
            super().__init__()

    def __init__(
        self,
        fields: List[FormField],
        title: Optional[str] = None,
        submit_label: str = "Submit",
    ):
        super().__init__()
        self.fields = fields
        self.title = title
        self.submit_label = submit_label
        self._widgets: Dict[str, Any] = {}
        self._errors: Dict[str, str] = {}

    def compose(self) -> ComposeResult:
        """Create form layout"""
        if self.title:
            yield Label(self.title, classes="form-title")

        for form_field in self.fields:
            container = Vertical(classes="field-container")

            # Add label
            container.mount(Label(f"{form_field.label}:"))

            # Create field widget
            widget = self._create_field_widget(form_field)
            container.mount(widget)
            self._widgets[form_field.name] = widget

            # Add help text
            if form_field.help_text:
                container.mount(Static(form_field.help_text, classes="help-text"))

            # Add error display
            error = Static("", classes="error-text")
            container.mount(error)

            yield container

        # Add submit button
        yield Button(self.submit_label, variant="primary", classes="submit-button")

    def _create_field_widget(self, field: FormField) -> Any:
        """Create widget for field type"""
        if field.type == "select" and field.choices:
            return Select(
                options=[(c, c) for c in field.choices],
                value=field.default,
                disabled=field.disabled,
            )
        elif field.type == "checkbox":
            return Checkbox(field.default or False, disabled=field.disabled)
        elif field.type == "textarea":
            return TextArea(
                value=field.default or "",
                placeholder=field.placeholder,
                disabled=field.disabled,
            )
        else:
            return Input(
                value=field.default or "",
                placeholder=field.placeholder,
                password=field.type == "password",
                disabled=field.disabled,
                validators=field.validators,
            )

    def validate(self) -> bool:
        """Validate form fields"""
        self._errors.clear()
        valid = True

        for form_field in self.fields:
            widget = self._widgets[form_field.name]
            value = widget.value

            # Check required
            if form_field.required and not value:
                self._errors[form_field.name] = "This field is required"
                valid = False
                continue

            # Run validators
            for validator in form_field.validators:
                try:
                    if not validator.validate(value):
                        self._errors[form_field.name] = validator.failure_description
                        valid = False
                        break
                except Exception as e:
                    self._errors[field.name] = str(e)
                    valid = False
                    break

        self.post_message(self.Validated(valid, dict(self._errors)))
        return valid

    def get_values(self) -> Dict[str, Any]:
        """Get form values"""
        return {field.name: self._widgets[field.name].value for field in self.fields}

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle submit button press"""
        if self.validate():
            self.post_message(self.Submitted(self.get_values()))
