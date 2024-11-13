"""AI module examples demonstrating LLM integrations"""

import asyncio
import os
from typing import Dict, List, Optional

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.style import Style

from pepperpy.ai.llm import LLMClient, Message, OpenRouterConfig, StackSpotConfig
from pepperpy.core.logging import get_logger

# Carregar variáveis de ambiente
load_dotenv()

logger = get_logger(__name__)

# Configurações dos providers
PROVIDER_CONFIGS = {
    "openrouter": {
        "env_prefix": "OPENROUTER_",
        "required_vars": ["API_KEY"],
        "optional_vars": ["MODEL", "SITE_URL", "SITE_NAME"],
        "defaults": {
            "model": "anthropic/claude-3-sonnet",
            "site_url": "https://github.com/felipepimentel/pepperpy",
            "site_name": "PepperPy",
        },
    },
    "stackspot": {
        "env_prefix": "STACKSPOT_",
        "required_vars": ["ACCOUNT_SLUG", "CLIENT_ID", "CLIENT_KEY", "QC_SLUG"],
        "optional_vars": ["BASE_URL", "AUTH_URL"],
        "defaults": {
            "base_url": "https://genai-code-buddy-api.stackspot.com/v1",
            "auth_url": "https://idm.stackspot.com",
        },
    },
}


def get_env_config(provider: str) -> Optional[Dict[str, str]]:
    """Get provider configuration from environment variables"""
    if provider not in PROVIDER_CONFIGS:
        return None

    config = PROVIDER_CONFIGS[provider]
    prefix = config["env_prefix"]

    # Verificar variáveis obrigatórias
    missing = []
    env_config = {}

    for var in config["required_vars"]:
        env_var = f"{prefix}{var}"
        value = os.getenv(env_var)
        if not value:
            missing.append(env_var)
        else:
            if value:
                env_config[var.lower()] = value
            else:
                missing.append(env_var)
    if missing:
        error_msg = f"Missing required environment variables for {provider}: {', '.join(missing)}"
        logger.sync.error(error_msg)
        return None

    for var in config["optional_vars"]:
        env_var = f"{prefix}{var}"
        value = os.getenv(env_var)
        if value:
            env_config[var.lower()] = value

    # Adicionar valores padrão
    for key, value in config["defaults"].items():
        if key not in env_config:
            env_config[key] = value

    return env_config


async def demo_chat_completion() -> None:
    """Demonstrate chat completion with different providers"""
    console = Console()

    # Mensagens de exemplo
    messages: List[Message] = [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "What are the key features of Python?"},
    ]

    try:
        # Demonstrar OpenRouter
        if openrouter_config := get_env_config("openrouter"):
            console.print("\n[bold cyan]Using OpenRouter Provider:[/]")
            client = LLMClient(OpenRouterConfig(**openrouter_config))
            await client.initialize()

            try:
                # Completar chat
                response = await client.complete(messages)
                console.print(
                    Panel(
                        response.content,
                        title="[bold]OpenRouter Response[/]",
                        border_style="blue",
                    )
                )

                # Demonstrar streaming
                console.print("\n[bold cyan]Streaming Response:[/]")
                console.print(Panel("", title="[bold]Streaming Demo[/]", border_style="yellow"))
                async for chunk in client.stream(messages):
                    console.print(chunk.content, end="", style=Style(color="cyan"))
                console.print()

            finally:
                await client.cleanup()

        # Demonstrar StackSpot
        if stackspot_config := get_env_config("stackspot"):
            console.print("\n[bold cyan]Using StackSpot AI Provider:[/]")
            client = LLMClient(StackSpotConfig(**stackspot_config))
            await client.initialize()

            try:
                response = await client.complete(messages)
                console.print(
                    Panel(
                        response.content,
                        title="[bold]StackSpot AI Response[/]",
                        border_style="green",
                    )
                )
            finally:
                await client.cleanup()

    except Exception as e:
        console.print(f"\n[bold red]Error:[/] {str(e)}", style="red")


if __name__ == "__main__":
    try:
        asyncio.run(demo_chat_completion())
    except KeyboardInterrupt:
        console = Console()
        console.print("\n[bold yellow]Demo finished![/] 👋")
