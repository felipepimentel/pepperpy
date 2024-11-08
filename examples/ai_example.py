import asyncio

from pepperpy.ai.module import AIModule
from pepperpy.ai.types import Message
from pepperpy.core.logging import get_logger
from pepperpy.core.resources import pepperpy_session

logger = get_logger("ai_example")


async def example_with_context() -> None:
    """Exemplo usando context manager"""
    async with AIModule.session() as ai:
        response = await ai.ask("What is the capital of France?")
        logger.info(f"Response: {response}")


async def example_with_resource_manager() -> None:
    """Exemplo usando gerenciador de recursos global"""
    async with pepperpy_session() as pepper:
        # Inicializa e gerencia automaticamente os recursos
        ai = await AIModule.create()
        await pepper.add("ai", ai)

        # Usa normalmente
        response = await ai.ask("Write a haiku about programming")
        logger.info(f"Response: {response}")

        # Cleanup automático ao sair do contexto


async def main() -> None:
    """Main example function"""
    logger.info("Starting PepperPy AI Example")

    # Exemplo 1: Usando context manager
    logger.info("\nExample with context manager:")
    await example_with_context()

    # Exemplo 2: Usando resource manager
    logger.info("\nExample with resource manager:")
    await example_with_resource_manager()

    # Exemplo 3: Uso simplificado para scripts rápidos
    logger.info("\nQuick usage example:")
    async with pepperpy_session() as pepper:
        ai = await AIModule.create()
        await pepper.add("ai", ai)

        messages = [
            Message(role="system", content="You are a quantum physics expert"),
            Message(role="user", content="Explain quantum entanglement simply"),
        ]
        response = await ai.generate(messages)
        logger.info(f"Expert Response: {response.content}")


if __name__ == "__main__":
    asyncio.run(main())
