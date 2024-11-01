from pepperpy.console import Console, CLI
from pepperpy.console.plugins import PluginManager
from pepperpy.console.plugins.logging import LoggingPlugin
from pepperpy.console.plugins.profiler import ProfilerPlugin
import logging
import time

# Setup
console = Console()
cli = CLI("myapp", version="1.0.0")
plugins = PluginManager()

# Registra plugins
plugins.register(LoggingPlugin)
plugins.register(ProfilerPlugin)

# Inicializa plugins
plugins.initialize(console, cli)

@cli.command()
def demo():
    """Demo command with logging."""
    logging.info("Starting demo...")
    
    for i in range(3):
        logging.debug(f"Processing item {i}")
        time.sleep(0.5)
        
    logging.info("Demo completed!")

@cli.command()
def heavy_task():
    """CPU intensive task for profiling."""
    result = 0
    for i in range(1000000):
        result += i * i
    return result

if __name__ == "__main__":
    cli.run() 