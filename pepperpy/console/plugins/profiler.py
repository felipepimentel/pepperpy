import cProfile
import pstats
from typing import Optional
from pathlib import Path
from . import ConsolePlugin, PluginMetadata
from ..core import Console
from ..cli import CLI

class ProfilerPlugin(ConsolePlugin):
    """Plugin para profiling de comandos."""
    
    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="profiler",
            version="1.0.0",
            description="Command profiling support",
            author="Pepperpy Team"
        )
    
    def initialize(self, console: Console, cli: Optional[CLI] = None) -> None:
        """Inicializa plugin de profiling."""
        if not cli:
            return
            
        @cli.group("profile", help="Profiling tools")
        def profile_group():
            pass
            
        @profile_group.command("run")
        def profile_command(command: str, output: Optional[Path] = None):
            """Profile a command execution."""
            profiler = cProfile.Profile()
            
            try:
                # Executa comando com profiling
                profiler.enable()
                cli.commands[command].callback()
                profiler.disable()
                
                # Gera relatório
                stats = pstats.Stats(profiler)
                stats.sort_stats('cumulative')
                
                if output:
                    stats.dump_stats(output)
                    console.success(f"Profile saved to {output}")
                else:
                    # Exibe no console
                    console.print("\n[bold]Profile Results:[/]")
                    stats.print_stats(20)  # Top 20 calls
                    
            except KeyError:
                console.error(f"Command '{command}' not found")
            except Exception as e:
                console.error(f"Profiling failed: {str(e)}")
    
    def cleanup(self) -> None:
        pass 