from pepperpy.console import Console, CLI
from pepperpy.console.plugins import PluginManager
from pepperpy.console.plugins.tqdm_integration import TQDMPlugin
from pepperpy.console.plugins.metrics import MetricsPlugin
import asyncio
import time

# Setup
console = Console()
cli = CLI("monitor", version="1.0.0")
plugins = PluginManager()

# Registra plugins
plugins.register(TQDMPlugin)
plugins.register(MetricsPlugin)
plugins.initialize(console, cli)

@cli.command()
async def process_with_monitoring():
    """Processa dados com monitoramento."""
    # Inicia monitoramento em background
    monitor_task = asyncio.create_task(
        console.monitor_resources(interval=0.5)
    )
    
    try:
        # Processamento com barra de progresso
        items = range(100)
        for item in console.tqdm(items, desc="Processing"):
            # Simula processamento
            await asyncio.sleep(0.1)
            
    finally:
        # Cancela monitoramento
        monitor_task.cancel()
        try:
            await monitor_task
        except asyncio.CancelledError:
            pass

@cli.command()
def batch_process():
    """Processamento em batch com diferentes estilos de progresso."""
    data = range(1000)
    
    # Usando TQDM
    console.print("\n[bold]Processing with TQDM:[/]")
    for item in console.tqdm(data, desc="TQDM Style"):
        time.sleep(0.001)
    
    # Usando Rich
    console.print("\n[bold]Processing with Rich:[/]")
    with console.status("Processing...") as status:
        for i, item in enumerate(data):
            if i % 100 == 0:
                status.update(f"Processed {i}/1000 items")
            time.sleep(0.001)

if __name__ == "__main__":
    cli.run() 