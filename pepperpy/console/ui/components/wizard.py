"""Wizard component for step-by-step configuration"""

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Pattern, Union

from ..styles import Style
from .base import Component, ComponentConfig


@dataclass
class WizardStep:
    """Configuration wizard step"""

    name: str
    prompt: str
    required: bool = True
    default: Any = None
    choices: Optional[List[str]] = None
    multiple: bool = False
    validator: Optional[Callable[[str], bool]] = None
    pattern: Optional[Union[str, Pattern]] = None
    help_text: Optional[str] = None
    type: str = "text"
    fields: Optional[Dict[str, tuple[str, Any]]] = None


class Wizard(Component):
    """Step-by-step configuration wizard"""

    def __init__(
        self,
        config: ComponentConfig,
        steps: List[WizardStep],
        title: Optional[str] = None,
        show_help: bool = True,
        style: Optional[Style] = None,
    ):
        super().__init__(config)
        self.steps = steps
        self.title = title
        self.show_help = show_help
        self.style = style or Style.DEFAULT
        self._current_step = 0
        self._values: Dict[str, Any] = {}

    async def render(self) -> None:
        """Render current wizard step"""
        if not self.config.visible:
            return

        # Render title if present
        if self.title:
            print(
                f"\033[{self.config.y};{self.config.x}H{self.style.apply()}{self.title}{self.style.reset()}"
            )

        # Render current step
        if self._current_step < len(self.steps):
            step = self.steps[self._current_step]
            y = self.config.y + (2 if self.title else 0)

            # Render prompt
            print(f"\033[{y};{self.config.x}H{step.prompt}")

            # Render help text if enabled
            if self.show_help and step.help_text:
                print(
                    f"\033[{y+1};{self.config.x}H{Style.INFO.apply()}{step.help_text}{Style.INFO.reset()}"
                )

            # Render choices if present
            if step.choices:
                for i, choice in enumerate(step.choices):
                    print(f"\033[{y+2+i};{self.config.x+2}H{i+1}. {choice}")

            # Render current value if any
            if step.name in self._values:
                value = self._values[step.name]
                print(f"\033[{y+2};{self.config.x}H> {value}")

    async def handle_input(self, value: str) -> bool:
        """Handle input for current step"""
        if self._current_step >= len(self.steps):
            return False

        step = self.steps[self._current_step]

        # Validate input
        if step.required and not value:
            return False

        if step.validator and not step.validator(value):
            return False

        if step.pattern:
            import re

            pattern = (
                step.pattern if isinstance(step.pattern, Pattern) else re.compile(step.pattern)
            )
            if not pattern.match(value):
                return False

        # Store value
        self._values[step.name] = value

        # Move to next step
        self._current_step += 1
        return True

    @property
    def values(self) -> Dict[str, Any]:
        """Get collected values"""
        return self._values.copy()

    @property
    def is_complete(self) -> bool:
        """Check if wizard is complete"""
        return self._current_step >= len(self.steps)
