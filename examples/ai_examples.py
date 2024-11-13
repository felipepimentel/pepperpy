"""AI module examples demonstrating LLM integrations"""

import asyncio
import os
from typing import Dict, Optional

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel

from pepperpy.ai.llm import LLMClient, OpenRouterConfig
from pepperpy.ai.llm.exceptions import LLMError
from pepperpy.core.logging import get_logger

# Carregar variáveis de ambiente
load_dotenv()
logger = get_logger(__name__)
console = Console()


def get_openrouter_config() -> Optional[Dict[str, str]]:
    """Get OpenRouter configuration from environment variables"""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        logger.sync.error("Missing OPENROUTER_API_KEY environment variable")
        return None

    if not api_key.startswith("sk-"):
        logger.sync.error("Invalid OpenRouter API key format. Key should start with 'sk-'")
        return None

    # Configuração com valores padrão
    config = {
        "api_key": api_key,
        "model": os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini"),  # Modelo mais acessível
        "site_url": os.getenv("SITE_URL", "https://github.com/felipepimentel/pepperpy"),
        "site_name": os.getenv("SITE_NAME", "PepperPy Demo"),
    }

    logger.sync.info(f"Using model: {config['model']}")
    return config


async def simple_chat_example() -> None:
    """Simple chat completion example using OpenRouter"""
    try:
        # Obter configuração
        config = get_openrouter_config()
        if not config:
            console.print("\n[red]Configuration Error:[/]")
            console.print("Please check your .env file and ensure the following variables are set:")
            console.print("- OPENROUTER_API_KEY (required, must start with 'sk-')")
            console.print("- OPENROUTER_MODEL (optional, defaults to openai/gpt-4o-mini)")
            console.print("- SITE_URL (optional)")
            console.print("- SITE_NAME (optional)")
            return

        # Criar e inicializar cliente
        client = LLMClient(OpenRouterConfig(**config))
        await client.initialize()

        try:
            # Enviar mensagem com contexto
            response = await client.complete(
                [
                    {
                        "role": "system",
                        "content": "You are a helpful AI assistant with expertise in Python programming.",
                    },
                    {
                        "role": "user",
                        "content": "What are the key features that make Python popular for AI development?",
                    },
                ]
            )

            # Exibir resposta com metadados
            console.print(
                Panel(
                    response.content,
                    title=f"[bold]AI Response using {response.model}[/]",
                    subtitle=f"Usage: {response.usage}",
                    border_style="green",
                )
            )

        finally:
            await client.cleanup()

    except LLMError as e:
        console.print("\n[bold red]Error:[/]")
        console.print(f"[red]{str(e)}[/]")
        if e.cause:  # LLMError já tem o atributo cause definido
            console.print(f"[red]Cause: {str(e.cause)}[/]")
    except Exception as e:
        console.print("\n[bold red]Error:[/]")
        console.print(f"[red]{str(e)}[/]")
        if e.__cause__:  # Usando __cause__ para exceções padrão
            console.print(f"[red]Cause: {str(e.__cause__)}[/]")


if __name__ == "__main__":
    try:
        asyncio.run(simple_chat_example())
    except KeyboardInterrupt:
        console.print("\n[yellow]Example finished![/] 👋")
