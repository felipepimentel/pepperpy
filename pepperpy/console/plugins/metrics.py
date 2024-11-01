from typing import Optional, Dict, Any
from ..plugins import ConsolePlugin, PluginMetadata
from ..core import Console
from ..cli import CLI
from rich.live import Live
from rich.table import Table
import time
import psutil
import asyncio

class MetricsPlugin(ConsolePlugin):
    """Plugin para métricas e monitoramento."""
    
    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="metrics",
            version="1.0.0",
            description="System metrics monitoring",
            author="Pepperpy Team"
        )
    
    def initialize(self, console: Console, cli: Optional[CLI] = None) -> None:
        """Inicializa plugin de métricas."""
        self.console = console
        
        async def monitor_resources(
            interval: float = 1.0,
            duration: Optional[float] = None
        ):
            """Monitora recursos do sistema."""
            start_time = time.time()
            table = Table(
                "Metric", "Value", 
                title="System Resources",
                border_style="blue"
            )
            
            with Live(table, refresh_per_second=4) as live:
                while True:
                    table.clear()
                    
                    # CPU
                    cpu_percent = psutil.cpu_percent(interval=0.1)
                    table.add_row("CPU Usage", f"{cpu_percent}%")
                    
                    # Memory
                    memory = psutil.virtual_memory()
                    table.add_row(
                        "Memory Usage",
                        f"{memory.percent}% ({memory.used / 1024 / 1024:.1f}MB)"
                    )
                    
                    # Disk
                    disk = psutil.disk_usage('/')
                    table.add_row(
                        "Disk Usage",
                        f"{disk.percent}% ({disk.used / 1024 / 1024 / 1024:.1f}GB)"
                    )
                    
                    if duration and time.time() - start_time > duration:
                        break
                        
                    await asyncio.sleep(interval)
        
        # Adiciona ao console
        console.monitor_resources = monitor_resources
        
        # Adiciona comandos CLI
        if cli:
            @cli.group("metrics")
            def metrics_group():
                """System metrics commands."""
                pass
                
            @metrics_group.command()
            def show(duration: int = 60):
                """Show system metrics."""
                asyncio.run(monitor_resources(duration=duration))
    
    def cleanup(self) -> None:
        pass 