"""Hook system for extensible behavior."""
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass
import asyncio
from enum import Enum

class HookType(Enum):
    """Types of hooks available."""
    BEFORE_REQUEST = "before_request"
    AFTER_REQUEST = "after_request"
    BEFORE_RESPONSE = "before_response"
    AFTER_RESPONSE = "after_response"
    ON_ERROR = "on_error"
    ON_SUCCESS = "on_success"

@dataclass
class HookContext:
    """Context passed to hook handlers."""
    hook_type: HookType
    data: Any
    metadata: dict = None

class HookManager:
    """Manage and execute hooks."""
    
    def __init__(self):
        self._hooks: Dict[HookType, List[Callable]] = {
            hook_type: [] for hook_type in HookType
        }
    
    def register(self, hook_type: HookType, handler: Callable) -> None:
        """Register a hook handler."""
        self._hooks[hook_type].append(handler)
    
    def unregister(self, hook_type: HookType, handler: Callable) -> None:
        """Unregister a hook handler."""
        if handlers := self._hooks.get(hook_type):
            self._hooks[hook_type] = [h for h in handlers if h != handler]
    
    async def trigger(self, hook_type: HookType, data: Any, metadata: dict = None) -> Any:
        """Trigger hooks of specified type."""
        context = HookContext(hook_type, data, metadata)
        
        for handler in self._hooks[hook_type]:
            try:
                if asyncio.iscoroutinefunction(handler):
                    context.data = await handler(context)
                else:
                    context.data = handler(context)
            except Exception as e:
                if hook_type != HookType.ON_ERROR:
                    await self.trigger(HookType.ON_ERROR, e, {
                        "original_hook": hook_type,
                        "original_data": data
                    })
                raise
        
        return context.data

class HookDecorator:
    """Decorator for registering hooks."""
    
    def __init__(self, manager: HookManager):
        self.manager = manager
    
    def before_request(self):
        def decorator(func):
            self.manager.register(HookType.BEFORE_REQUEST, func)
            return func
        return decorator
    
    def after_request(self):
        def decorator(func):
            self.manager.register(HookType.AFTER_REQUEST, func)
            return func
        return decorator
    
    def on_error(self):
        def decorator(func):
            self.manager.register(HookType.ON_ERROR, func)
            return func
        return decorator 