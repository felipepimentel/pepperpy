from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt


@dataclass
class WizardStep:
    """Configuration wizard step"""

    name: str
    prompt: str
    type: type = str
    choices: Optional[List[str]] = None
    default: Any = None
    required: bool = True


class ConfigWizard:
    """Interactive configuration wizard"""

    def __init__(self, console: Console):
        self._console = console

    async def run(self, title: str, steps: List[WizardStep]) -> Dict[str, Any]:
        """Run configuration wizard"""
        self._console.print(Panel(f"[bold blue]{title}[/]"))

        config = {}
        for step in steps:
            value = await self._get_input(step)
            if value is not None:
                config[step.name] = value

        return config

    async def _get_input(self, step: WizardStep) -> Any:
        """Get user input for a wizard step"""
        kwargs = {"default": step.default}

        if step.choices:
            kwargs["choices"] = step.choices

        while True:
            try:
                value = Prompt.ask(step.prompt, **kwargs)

                if not value and step.required:
                    self._console.print("[red]This field is required[/]")
                    continue

                if not value and not step.required:
                    return None

                return step.type(value)

            except ValueError:
                self._console.print(f"[red]Invalid input. Expected type: {step.type.__name__}[/]")
