import logging
from typing import Optional
from rich.logging import RichHandler
from ..core import Console
from ..cli import CLI
from . import ConsolePlugin, PluginMetadata

class LoggingPlugin(ConsolePlugin):
    """Plugin para integração com logging."""
    
    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="logging",
            version="1.0.0",
            description="Rich logging integration",
            author="Pepperpy Team"
        )
    
    def initialize(self, console: Console, cli: Optional[CLI] = None) -> None:
        """Configura logging com Rich."""
        # Configura handler Rich
        handler = RichHandler(
            console=console._console,
            show_time=True,
            show_path=True
        )
        
        # Configura logging
        logging.basicConfig(
            level=logging.INFO,
            format="%(message)s",
            datefmt="[%X]",
            handlers=[handler]
        )
        
        # Adiciona comandos CLI se disponível
        if cli:
            @cli.group("log", help="Logging management")
            def log_group():
                pass
                
            @log_group.command("level")
            def set_level(level: str):
                """Set logging level."""
                numeric_level = getattr(logging, level.upper())
                logging.getLogger().setLevel(numeric_level)
                console.success(f"Logging level set to {level}")
    
    def cleanup(self) -> None:
        """Limpa handlers de logging."""
        logging.getLogger().handlers = [] 