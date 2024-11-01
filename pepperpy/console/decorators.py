from functools import wraps
from typing import Callable, Any, Optional, Union
import time
from rich.progress import track
from .core import Console
import asyncio

class ConsoleDecorators:
    """Decoradores para funcionalidades de console."""
    
    def __init__(self, console: Console):
        self.console = console
    
    def progress(
        self,
        description: str = "Processing",
        total: Optional[int] = None,
        show_eta: bool = True,
        transient: bool = False
    ):
        """Decorator para adicionar barra de progresso."""
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs) -> Any:
                with self.console.status(description) as status:
                    try:
                        result = func(*args, **kwargs)
                        status.update(f"✅ {description} completed")
                        return result
                    except Exception as e:
                        status.update(f"❌ {description} failed: {str(e)}")
                        raise
            return wrapper
        return decorator
    
    def timer(
        self,
        show_args: bool = False,
        style: str = "info"
    ):
        """Decorator para medir e exibir tempo de execução."""
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            async def async_wrapper(*args, **kwargs) -> Any:
                start = time.perf_counter()
                try:
                    result = await func(*args, **kwargs)
                    elapsed = time.perf_counter() - start
                    
                    msg = f"⏱️ {func.__name__}"
                    if show_args:
                        msg += f"({args}, {kwargs})"
                    msg += f" completed in {elapsed:.2f}s"
                    
                    self.console.print(msg, style=style)
                    return result
                except Exception as e:
                    elapsed = time.perf_counter() - start
                    self.console.print(
                        f"❌ {func.__name__} failed after {elapsed:.2f}s: {str(e)}",
                        style="error"
                    )
                    raise
            
            @wraps(func)
            def sync_wrapper(*args, **kwargs) -> Any:
                start = time.perf_counter()
                try:
                    result = func(*args, **kwargs)
                    elapsed = time.perf_counter() - start
                    self.console.print(
                        f"⏱️ {func.__name__} completed in {elapsed:.2f}s",
                        style=style
                    )
                    return result
                except Exception as e:
                    elapsed = time.perf_counter() - start
                    self.console.print(
                        f"❌ {func.__name__} failed after {elapsed:.2f}s: {str(e)}",
                        style="error"
                    )
                    raise
            
            return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
        return decorator
    
    def confirm(
        self,
        message: str = "Continue?",
        style: str = "warning",
        abort_message: Optional[str] = None
    ):
        """Decorator para confirmação do usuário."""
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs) -> Any:
                if self.console.confirm(message, style=style):
                    return func(*args, **kwargs)
                if abort_message:
                    self.console.print(abort_message, style="warning")
            return wrapper
        return decorator
    
    def log_calls(
        self,
        level: str = "info",
        show_args: bool = False,
        show_result: bool = False
    ):
        """Decorator para logar chamadas de função."""
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs) -> Any:
                func_name = func.__name__
                
                # Log entrada
                msg = f"➡️ Calling {func_name}"
                if show_args:
                    msg += f" with args={args}, kwargs={kwargs}"
                self.console.print(msg, style=level)
                
                try:
                    result = func(*args, **kwargs)
                    
                    # Log saída
                    msg = f"✅ {func_name} completed"
                    if show_result:
                        msg += f" with result: {result}"
                    self.console.print(msg, style=level)
                    
                    return result
                except Exception as e:
                    self.console.print(
                        f"❌ {func_name} failed: {str(e)}",
                        style="error"
                    )
                    raise
            return wrapper
        return decorator