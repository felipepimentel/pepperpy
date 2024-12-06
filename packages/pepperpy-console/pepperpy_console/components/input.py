"""Input component implementation."""

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from ..base.component import BaseComponent
from ..base.console import Console


@dataclass
class InputConfig:
    """Input configuration."""

    prompt: str = "> "
    default: str | None = None
    validator: Callable[[str], bool] | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class Input(BaseComponent):
    """Input component."""

    def __init__(self, console: Console, config: InputConfig | None = None) -> None:
        """Initialize input component."""
        super().__init__()
        self.console = console
        self.config = config or InputConfig()
        self._value: str = ""

    @property
    def value(self) -> str:
        """Get current input value."""
        return self._value

    @value.setter
    def value(self, value: str) -> None:
        """Set input value."""
        self._value = value

    async def initialize(self) -> None:
        """Initialize input component."""
        await super().initialize()

    async def cleanup(self) -> None:
        """Cleanup input component."""
        await super().cleanup()

    async def read(self, prompt: str | None = None) -> str:
        """Read input from console."""
        actual_prompt = prompt or self.config.prompt
        value = input(actual_prompt)

        if not value and self.config.default is not None:
            return self.config.default

        if self.config.validator and not self.config.validator(value):
            raise ValueError("Invalid input")

        self._value = value
        return value
