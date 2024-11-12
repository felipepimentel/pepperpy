"""Debugging utilities"""

import asyncio
import functools
import inspect
import sys
import traceback
from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, Callable, Dict, TypeVar

from pepperpy.core.logging import get_logger

T = TypeVar("T")


class AsyncDebugger:
    """Async function debugger"""

    def __init__(self, name: str):
        self.name = name
        self._logger = get_logger(__name__)
        self._traces: Dict[str, list] = {}
        self._active = False

    @asynccontextmanager
    async def trace(self) -> AsyncIterator["AsyncDebugger"]:
        """Trace execution with debug information

        Returns:
            AsyncIterator[AsyncDebugger]: Debugger instance
        """
        self._active = True
        try:
            yield self
        finally:
            self._active = False
            if self._traces:
                await self._logger.debug(f"Debug trace for {self.name}", traces=self._traces)

    def _get_trace_info(self) -> Dict[str, Any]:
        """Get current trace information"""
        frame = sys._getframe(2)
        info = {
            "file": frame.f_code.co_filename,
            "function": frame.f_code.co_name,
            "line": frame.f_lineno,
            "locals": {k: str(v) for k, v in frame.f_locals.items() if not k.startswith("_")},
        }
        return info

    def debug_function(self, func: Callable[..., T]) -> Callable[..., T]:
        """Decorator for debugging async functions

        Args:
            func: Function to debug

        Returns:
            Callable[..., T]: Decorated function
        """
        if not asyncio.iscoroutinefunction(func):
            raise ValueError("Can only debug async functions")

        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            if not self._active:
                return await func(*args, **kwargs)

            # Get function info
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            func_info = {
                "name": func.__name__,
                "args": str(bound_args.arguments),
                "source": inspect.getsource(func),
            }

            try:
                # Record entry
                trace_id = f"{func.__name__}_{id(func)}"
                self._traces[trace_id] = [{"event": "enter", "info": func_info}]

                # Execute function
                result = await func(*args, **kwargs)

                # Record success
                self._traces[trace_id].append({"event": "exit", "info": {"result": str(result)}})

                return result

            except Exception as e:
                # Record error
                self._traces[trace_id].append(
                    {
                        "event": "error",
                        "info": {
                            "type": type(e).__name__,
                            "message": str(e),
                            "traceback": traceback.format_exc(),
                        },
                    }
                )
                raise

        return wrapper
