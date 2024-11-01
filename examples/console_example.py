from pepperpy.console import Console, CLI, ProgressBar, ProgressConfig, TaskConfig
import time
import random

console = Console()
progress = ProgressBar(ProgressConfig(
    style="rich",
    show_speed=True,
    show_eta=True
))

cli = CLI("myapp", version="1.0.0")

@cli.command(help="Demonstração interativa")
def demo():
    # Demonstração de tabela live
    with console.live_table(
        ["Métrica", "Valor"],
        title="Monitoramento",
        border_style="blue"
    ) as add_row:
        for _ in range(5):
            add_row(
                "CPU",
                f"{random.randint(0, 100)}%"
            )
            time.sleep(0.5)
    
    # Demonstração de prompt dict
    config = console.prompt_dict({
        "debug": False,
        "log_level": ["INFO", "DEBUG", "WARNING"],
        "max_retries": 3
    })
    console.dict_view(config, "Configuração:")
    
    # Demonstração de progresso com configs específicas
    with progress.task_group() as tasks:
        # Download task
        tasks.add_task("download", TaskConfig(
            description="Baixando dados",
            total=100,
            start_message="Iniciando download...",
            complete_message="✅ Download completo em {elapsed}"
        ))
        
        # Process task
        tasks.add_task("process", TaskConfig(
            description="Processando",
            total=50,
            start_message="Iniciando processamento...",
            complete_message="✅ Processamento completo em {elapsed}"
        ))
        
        try:
            for i in range(100):
                tasks.update("download")
                if i % 2 == 0:
                    tasks.update("process")
                time.sleep(0.05)
                
            tasks.complete_task("download")
            tasks.complete_task("process")
            
        except Exception as e:
            tasks.error_task("download", e)
            tasks.error_task("process", e)

if __name__ == "__main__":
    cli.run()