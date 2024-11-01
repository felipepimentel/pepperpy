from pepperpy.console import Console, CLI
from pepperpy.console.decorators import ConsoleDecorators
import asyncio
import time
import random

console = Console()
decorators = ConsoleDecorators(console)
cli = CLI("myapp", version="1.0.0")

@cli.command()
@decorators.timer(show_args=True)
@decorators.confirm("Iniciar processamento?")
async def process_data():
    """Processa dados com feedback rico."""
    with console.status("Inicializando...") as status:
        await asyncio.sleep(1)
        status.update("Carregando dados...")
        
        data = await load_data()
        status.update("Processando dados...")
        
        with console.live_table(
            ["Etapa", "Status", "Tempo"],
            title="Progresso do Processamento"
        ) as add_row:
            for step in ["Validação", "Transformação", "Agregação"]:
                start = time.time()
                await asyncio.sleep(random.uniform(0.5, 1.5))
                elapsed = time.time() - start
                add_row(step, "✅ Completo", f"{elapsed:.2f}s")
        
        return data

@decorators.log_calls(show_result=True)
async def load_data():
    """Carrega dados com logging automático."""
    await asyncio.sleep(1)
    return {"status": "success", "items": 100}

@cli.command()
@decorators.timer()
def interactive_config():
    """Configuração interativa com feedback rico."""
    config = console.prompt_dict({
        "ambiente": ["dev", "prod", "test"],
        "debug": False,
        "max_retries": 3,
        "timeout": 30
    })
    
    console.tree({
        "Configuração": {
            "Ambiente": config["ambiente"],
            "Debug": config["debug"],
            "Parâmetros": {
                "Max Retries": config["max_retries"],
                "Timeout": config["timeout"]
            }
        }
    }, "📝 Configuração Final")
    
    return config

if __name__ == "__main__":
    cli.run() 