from dataclasses import dataclass, field
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Type, Union

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn


@dataclass
class CommandConfig:
    """Configuration for CLI command"""

    name: str
    help: str
    callback: Callable
    options: List[Dict[str, Any]] = field(default_factory=list)
    arguments: List[Dict[str, Any]] = field(default_factory=list)
    aliases: List[str] = field(default_factory=list)
    hidden: bool = False


class CommandBuilder:
    """Builder for CLI commands"""

    def __init__(self, name: str, help: str = "", hidden: bool = False):
        self.config = CommandConfig(
            name=name, help=help, callback=lambda: None, hidden=hidden
        )

    def option(
        self,
        name: str,
        type: Type = str,
        help: str = "",
        default: Any = None,
        required: bool = False,
    ) -> "CommandBuilder":
        """Add command option"""
        self.config.options.append(
            {
                "name": name,
                "type": type,
                "help": help,
                "default": default,
                "required": required,
            }
        )
        return self

    def argument(
        self, name: str, type: Type = str, help: str = "", required: bool = True
    ) -> "CommandBuilder":
        """Add command argument"""
        self.config.arguments.append(
            {"name": name, "type": type, "help": help, "required": required}
        )
        return self

    def alias(self, *names: str) -> "CommandBuilder":
        """Add command aliases"""
        self.config.aliases.extend(names)
        return self

    def callback(self, func: Callable) -> Callable:
        """Set command callback"""
        self.config.callback = func
        return func


class CLIBuilder:
    """Builder for CLI applications"""

    def __init__(self, name: str, help: str = "", version: str = "0.1.0"):
        self.app = typer.Typer(name=name, help=help, rich_markup_mode="rich")
        self.version = version
        self.console = Console()
        self._commands: Dict[str, CommandConfig] = {}

        # Add version command
        @self.app.callback()
        def version_callback(
            version: bool = typer.Option(
                False, "--version", "-v", help="Show version and exit"
            ),
        ):
            if version:
                self.console.print(f"{name} version: {self.version}")
                raise typer.Exit()

    def command(
        self, name: Optional[str] = None, help: str = "", hidden: bool = False
    ) -> Union[CommandBuilder, Callable]:
        """Create new command"""

        def decorator(func: Callable) -> Callable:
            cmd_name = name or func.__name__
            builder = CommandBuilder(cmd_name, help, hidden)

            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            builder.callback(wrapper)
            self._commands[cmd_name] = builder.config

            # Create command
            cmd = typer.Command(
                name=cmd_name,
                help=help,
                callback=self._wrap_callback(wrapper),
                hidden=hidden,
            )

            self.app.command()(cmd)
            return wrapper

        if callable(name):
            func = name
            name = None
            return decorator(func)
        return decorator

    def _wrap_callback(self, func: Callable) -> Callable:
        """Wrap command callback with progress and error handling"""

        async def wrapper(*args, **kwargs):
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console,
            ) as progress:
                try:
                    task = progress.add_task(f"Running {func.__name__}...", total=None)
                    result = await func(*args, **kwargs)
                    progress.update(task, completed=True)
                    return result
                except Exception as err:
                    self.console.print(f"[red]Error:[/red] {str(err)}")
                    raise typer.Exit(1) from err

        return wrapper

    def build(self) -> typer.Typer:
        """Build CLI application"""
        return self.app
