"""CLI application"""

from typing import Any, Dict, List, Optional

import typer
from rich.console import Console
from rich.prompt import Confirm, Prompt
from typer.core import TyperCommand

from pepperpy.core.logging import get_logger

from .exceptions import ArgumentError, CLIError, CommandError


class CLIApp:
    """CLI application"""

    def __init__(self):
        self._logger = get_logger(__name__)
        self._app = typer.Typer()
        self._console = Console()
        self._commands: Dict[str, typer.Typer] = {}

    def command(self, name: str) -> typer.Typer:
        """Register command group

        Args:
            name: Command name

        Returns:
            typer.Typer: Command group
        """
        if name in self._commands:
            raise CommandError(f"Command already exists: {name}")

        command = typer.Typer()
        self._commands[name] = command
        self._app.add_typer(command, name=name)
        return command

    async def run(self) -> None:
        """Run CLI application"""
        try:
            await self._logger.info("Starting CLI application")
            self._app()
        except Exception as e:
            await self._logger.error(f"CLI error: {str(e)}")
            raise CLIError(f"CLI error: {str(e)}", cause=e)

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
        try:
            return Prompt.ask(
                prompt=message,
                default=default,
                **kwargs,
            )
        except Exception as e:
            raise ArgumentError(f"Invalid input: {str(e)}", cause=e)

    def confirm(self, message: str, default: bool = False) -> bool:
        """Ask for confirmation

        Args:
            message: Message to print
            default: Default value

        Returns:
            bool: True if confirmed
        """
        try:
            return Confirm.ask(message, default=default, console=self._console)
        except Exception as e:
            raise ArgumentError(f"Invalid input: {str(e)}", cause=e)

    def add_argument(
        self,
        name: str,
        type_: type,
        help_: str,
        default: Optional[Any] = None,
        required: bool = False,
    ) -> None:
        """Add command line argument

        Args:
            name: Argument name
            type_: Argument type
            help_: Help text
            default: Default value
            required: Whether argument is required
        """
        try:
            arg_info = typer.Argument(default=default if not required else ..., help=help_)

            @self._app.command(name=name, help=help_)
            def callback(value: type_ = arg_info) -> None:
                pass

        except Exception as e:
            raise ArgumentError(f"Failed to add argument: {str(e)}", cause=e)

    def parse_args(self, args: Optional[List[str]] = None) -> Dict[str, Any]:
        """Parse command line arguments

        Args:
            args: Command line arguments

        Returns:
            Dict[str, Any]: Parsed arguments
        """
        try:
            # Criar um novo contexto para o comando
            command = TyperCommand(name="", callback=lambda: None)
            ctx = typer.Context(command)
            if args:
                ctx.args = args
            return ctx.params
        except Exception as e:
            raise ArgumentError(f"Failed to parse arguments: {str(e)}", cause=e)


# Global CLI application instance
app = CLIApp()
