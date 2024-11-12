"""CLI application implementation"""

from typing import Any, Callable, Dict, Optional

import typer
from rich.console import Console
from rich.prompt import Confirm, Prompt

from .config import CLIConfig
from .exceptions import CLIError
from .types import Command


class CLI:
    """Command Line Interface"""

    def __init__(self, config: Optional[CLIConfig] = None):
        self.config = config or CLIConfig()
        self.app = typer.Typer(
            name=self.config.name, help=self.config.description, rich_markup_mode="rich"
        )
        self.console = Console()
        self._commands: Dict[str, Command] = {}

    def command(
        self, name: Optional[str] = None, help: Optional[str] = None, **kwargs: Any
    ) -> Callable:
        """Command decorator"""

        def decorator(func: Callable) -> Callable:
            cmd_name = name or func.__name__
            command = Command(
                name=cmd_name, callback=func, help=help or func.__doc__ or "", **kwargs
            )
            self._commands[cmd_name] = command

            # Create typer command
            typer_command = self.app.command(name=cmd_name, help=command.help, **kwargs)
            return typer_command(func)

        return decorator

    def option(self, *param_decls: str, help: Optional[str] = None, **kwargs: Any) -> Callable:
        """Option decorator"""
        return typer.Option(*param_decls, help=help, **kwargs)

    def argument(self, *param_decls: str, help: Optional[str] = None, **kwargs: Any) -> Callable:
        """Argument decorator"""
        return typer.Argument(*param_decls, help=help, **kwargs)

    def run(self) -> None:
        """Run CLI application"""
        try:
            self.app()
        except Exception as e:
            raise CLIError(f"CLI execution failed: {str(e)}", cause=e)

    def prompt(self, message: str, type: Any = str, default: Any = None, **kwargs: Any) -> Any:
        """Prompt for input"""
        return Prompt.ask(message, default=default, type=type, **kwargs)

    def confirm(self, message: str, default: bool = False, **kwargs: Any) -> bool:
        """Prompt for confirmation"""
        return Confirm.ask(message, default=default, **kwargs)

    def print(self, *objects: Any, style: Optional[str] = None, **kwargs: Any) -> None:
        """Print to console"""
        self.console.print(*objects, style=style, **kwargs)

    def print_json(self, data: Any, indent: int = 2, **kwargs: Any) -> None:
        """Print JSON data"""
        self.console.print_json(data, indent=indent, **kwargs)
