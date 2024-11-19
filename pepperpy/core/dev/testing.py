"""Testing utilities"""

import asyncio
from typing import Any, Callable

from pepperpy.core.logging import get_logger

logger = get_logger(__name__)


async def async_test(
    test_func: Callable[..., Any],
    *args: Any,
    **kwargs: Any,
) -> None:
    """Run async test function"""
    try:
        await logger.info(f"Running test: {test_func.__name__}")
        result = await test_func(*args, **kwargs)
        await logger.info(
            f"Test {test_func.__name__} completed",
            result=result,
        )
    except Exception as e:
        await logger.error(
            f"Test {test_func.__name__} failed",
            error=str(e),
        )
        raise


def run_async_test(
    test_func: Callable[..., Any],
    *args: Any,
    **kwargs: Any,
) -> None:
    """Run async test in event loop"""
    try:
        # Criar novo event loop para garantir execução limpa
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            # Executar teste de forma síncrona
            loop.run_until_complete(async_test(test_func, *args, **kwargs))
        finally:
            # Limpar recursos
            loop.close()
            
    except Exception as e:
        # Usar versão síncrona do logger para erro final
        sync_logger = get_logger(__name__, async_=False)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(
                sync_logger.error(
                    f"Failed to run test {test_func.__name__}",
                    error=str(e),
                )
            )
        finally:
            loop.close()
        raise
