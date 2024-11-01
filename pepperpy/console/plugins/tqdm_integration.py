from typing import Optional, Any, Iterable
from ..plugins import ConsolePlugin, PluginMetadata
from ..core import Console
from ..cli import CLI
from tqdm.auto import tqdm
from rich.progress import Progress

class TQDMPlugin(ConsolePlugin):
    """Plugin para integração com TQDM."""
    
    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="tqdm",
            version="1.0.0",
            description="TQDM integration for progress bars",
            author="Pepperpy Team"
        )
    
    def initialize(self, console: Console, cli: Optional[CLI] = None) -> None:
        """Inicializa integração com TQDM."""
        # Adiciona métodos ao console
        def progress_wrap(
            iterable: Iterable,
            desc: Optional[str] = None,
            total: Optional[int] = None,
            **kwargs
        ) -> Iterable:
            """Wrapper para TQDM com estilo Rich."""
            with Progress() as progress:
                task = progress.add_task(desc or "", total=total)
                for item in iterable:
                    yield item
                    progress.update(task, advance=1)
                    
        console.tqdm = progress_wrap
        
        # Adiciona comandos CLI se disponível
        if cli:
            @cli.group("progress")
            def progress_group():
                """Progress bar management."""
                pass
                
            @progress_group.command()
            def style(style: str = "auto"):
                """Set TQDM style (auto/rich/minimal)."""
                tqdm._instances.clear()  # Reset instances
                if style == "rich":
                    console.print("Using Rich progress bars")
                elif style == "minimal":
                    console.print("Using minimal progress bars")
                else:
                    console.print("Using automatic progress bars")
    
    def cleanup(self) -> None:
        """Limpa instâncias TQDM."""
        tqdm._instances.clear() 