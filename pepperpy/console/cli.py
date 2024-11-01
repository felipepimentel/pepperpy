from typing import Optional, Callable, Dict, Any, List, Type, Union
import click
from rich.console import Console
from .core import Console as PeppyConsole
import importlib
from pathlib import Path

class CommandGroup:
    """Grupo de comandos relacionados."""
    
    def __init__(
        self,
        name: str,
        help: Optional[str] = None,
        aliases: Optional[List[str]] = None
    ):
        self.name = name
        self.help = help
        self.aliases = aliases or []
        self.commands: Dict[str, click.Command] = {}
        self.default_command: Optional[str] = None
    
    def command(
        self,
        name: Optional[str] = None,
        help: Optional[str] = None,
        aliases: Optional[List[str]] = None,
        default: bool = False
    ) -> Callable:
        """Decorator para registrar comandos no grupo."""
        def decorator(func: Callable) -> Callable:
            cmd_name = name or func.__name__
            cmd = click.Command(
                name=cmd_name,
                help=help,
                callback=func,
                aliases=aliases or []
            )
            self.commands[cmd_name] = cmd
            
            if default:
                self.default_command = cmd_name
                
            return func
        return decorator

class CLI:
    """Builder avançado para CLIs."""
    
    def __init__(
        self,
        name: str,
        help: Optional[str] = None,
        version: Optional[str] = None,
        plugins: Optional[List[str]] = None,
        config_file: Optional[Union[str, Path]] = None,
        auto_env_vars: bool = True
    ):
        self.name = name
        self.help = help
        self.version = version
        self.groups: Dict[str, CommandGroup] = {}
        self.commands: Dict[str, click.Command] = {}
        self.console = PeppyConsole()
        self.plugins = {}
        self.config_file = Path(config_file) if config_file else None
        self.auto_env_vars = auto_env_vars
        
        if plugins:
            self._load_plugins(plugins)
        
        if version:
            self.add_version_command()
        
        if config_file:
            self.add_config_commands()
            
        self.add_completion()
    
    def add_version_command(self):
        """Adiciona comando de versão."""
        @self.command(name="version", help="Show version info")
        def version():
            self.console.print(f"{self.name} version {self.version}")
    
    def add_config_commands(self):
        """Adiciona comandos de configuração."""
        config_group = self.group("config", help="Configuration management")
        
        @config_group.command(name="show", help="Show current configuration")
        def show_config():
            if self.config_file and self.config_file.exists():
                config = self._load_config()
                self.console.tree(config, "Current Configuration")
            else:
                self.console.warning("No configuration file found")
        
        @config_group.command(name="init", help="Initialize configuration file")
        def init_config():
            if not self.config_file.exists():
                self._save_config({})
                self.console.success(f"Created config file: {self.config_file}")
            else:
                self.console.warning("Configuration file already exists")
    
    def group(
        self,
        name: str,
        help: Optional[str] = None,
        aliases: Optional[List[str]] = None
    ) -> CommandGroup:
        """Cria novo grupo de comandos."""
        group = CommandGroup(name, help, aliases)
        self.groups[name] = group
        return group
    
    def command(
        self,
        name: Optional[str] = None,
        help: Optional[str] = None,
        aliases: Optional[List[str]] = None
    ) -> Callable:
        """Decorator para registrar comandos globais."""
        def decorator(func: Callable) -> Callable:
            cmd_name = name or func.__name__
            
            @click.command(
                name=cmd_name,
                help=help,
                context_settings={"auto_envvar_prefix": self.name.upper()} if self.auto_env_vars else None
            )
            @click.pass_context
            def wrapper(ctx: click.Context, *args, **kwargs) -> Any:
                ctx.obj = ctx.obj or {}
                ctx.obj["console"] = self.console
                ctx.obj["config"] = self._load_config() if self.config_file else {}
                
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    self.console.error(f"Command failed: {str(e)}")
                    if ctx.obj.get("debug"):
                        import traceback
                        self.console.print(traceback.format_exc())
                    ctx.exit(1)
                    
            self.commands[cmd_name] = wrapper
            return wrapper
        return decorator
    
    def _load_config(self) -> dict:
        """Carrega configuração do arquivo."""
        if not self.config_file or not self.config_file.exists():
            return {}
            
        import toml
        return toml.load(self.config_file)
    
    def _save_config(self, config: dict):
        """Salva configuração no arquivo."""
        import toml
        with open(self.config_file, "w") as f:
            toml.dump(config, f)
    
    def run(self, auto_envvar_prefix: Optional[str] = None) -> None:
        """Executa a CLI."""
        cli = click.Group(
            name=self.name,
            help=self.help,
            context_settings={
                "auto_envvar_prefix": auto_envvar_prefix or self.name.upper()
            } if self.auto_env_vars else {}
        )
        
        # Adiciona comandos globais
        for cmd in self.commands.values():
            cli.add_command(cmd)
        
        # Adiciona grupos de comandos
        for group in self.groups.values():
            group_cli = click.Group(
                name=group.name,
                help=group.help,
                aliases=group.aliases
            )
            
            for cmd in group.commands.values():
                group_cli.add_command(cmd)
                
            if group.default_command:
                group_cli.set_default_command(
                    group.commands[group.default_command]
                )
                
            cli.add_command(group_cli)
            
        cli()