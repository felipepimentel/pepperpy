"""CLI application"""

from typing import Any, Callable, Optional

import typer
from rich.console import Console
from rich.prompt import Confirm, Prompt

from pepperpy.core.logging import get_logger


class CLIApp:
    """CLI application"""

    def __init__(self):
        self._logger = get_logger(__name__)
        self._app = typer.Typer()
        self._console = Console()

    def command(self, name: Optional[str] = None) -> Callable:
        """Register command

        Args:
            name: Command name

        Returns:
            Callable: Command decorator
        """
        return self._app.command(name=name)

    async def run(self) -> None:
        """Run CLI application"""
        try:
            self._app()
        except Exception as e:
            await self._logger.error(f"CLI error: {str(e)}")
            raise

    def print(self, message: str, **kwargs: Any) -> None:
        """Print message to console

        Args:
            message: Message to print
            kwargs: Additional arguments for rich.print
        """
        self._console.print(message, **kwargs)

    def ask(
        self,
        message: str,
        type_: type = str,
        default: Optional[Any] = None,
        **kwargs: Any,
    ) -> Any:
        """Ask for user input

        Args:
            message: Message to print
            type_: Expected input type
            default: Default value
            kwargs: Additional arguments for prompt

        Returns:
            Any: User input
        """
        return Prompt.ask(
            prompt=message,
            default=default,
            **kwargs,
        )

    def confirm(self, message: str, default: bool = False) -> bool:
        """Ask for confirmation

        Args:
            message: Message to print
            default: Default value

        Returns:
            bool: True if confirmed
        """
        return Confirm.ask(message, default=default, console=self._console)


# Global CLI application instance
app = CLIApp()
