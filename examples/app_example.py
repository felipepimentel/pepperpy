from pepperpy import Pepperpy
from pepperpy.plugins.database import DatabasePlugin
from pepperpy.plugins.cache import RedisPlugin
from pepperpy.plugins.metrics import MetricsPlugin

# Configuração via dict
config = {
    "database": {
        "url": "postgresql://localhost/myapp",
        "pool_size": 5
    },
    "cache": {
        "url": "redis://localhost",
        "ttl": 300
    },
    "metrics": {
        "enabled": True,
        "interval": 60
    }
}

# Inicialização com plugins
app = Pepperpy(
    config=config,
    plugins=[
        DatabasePlugin,
        RedisPlugin,
        MetricsPlugin
    ]
)

# Criação de CLI
cli = app.create_cli(
    "myapp",
    version="1.0.0",
    auto_env_vars=True
)

@cli.command()
async def process():
    """Processa dados com recursos integrados."""
    with app.console.status("Processing..."):
        # Cache automático
        data = await app.cache.get("my_data")
        if not data:
            data = await app.plugins.get("database").fetch_data()
            await app.cache.set("my_data", data, ttl=300)
        
        # Métricas automáticas
        metrics = app.plugins.get("metrics")
        metrics.increment("process_count")
        
        # Eventos
        await app.events.emit("data.processed", data)
        
        app.console.success("Processing complete!")

if __name__ == "__main__":
    cli.run() 