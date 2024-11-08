from typing import Any, Callable, Dict, Optional

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt


class Menu:
    """Interactive menu component with rich formatting"""

    def __init__(self, console: Console):
        self._console = console

    async def show(
        self, title: str, options: Dict[str, Callable], description: Optional[str] = None
    ) -> Any:
        """Display interactive menu and handle selection"""
        while True:
            self._console.print(Panel(title, subtitle=description, style="bold blue"))

            # Display options
            for idx, (label, _) in enumerate(options.items(), 1):
                self._console.print(f"{idx}. {label}")

            # Get selection
            choice = Prompt.ask(
                "Select an option", choices=[str(i) for i in range(1, len(options) + 1)]
            )

            # Execute selected action
            action = list(options.values())[int(choice) - 1]
            result = await action()

            if not Confirm.ask("Would you like to perform another action?"):
                return result
