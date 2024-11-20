"""Agent examples demonstrating different AI agent capabilities"""

import asyncio

from pepperpy.ai import AIClient
from pepperpy.core.logging import get_logger

logger = get_logger(__name__)


async def demonstrate_research_agent() -> None:
    """Demonstrate research agent capabilities"""
    try:
        print("\n🤖 Initializing Research Agent...")

        # Criar cliente AI com configuração padrão
        client = AIClient()
        await client.initialize()

        # Implementar lógica do agente aqui
        print("✅ Research agent initialized")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        await logger.error("Research demonstration failed", error=str(e))
    finally:
        if "client" in locals():
            await client.cleanup()


if __name__ == "__main__":
    asyncio.run(demonstrate_research_agent())
