"""Main application class with middleware and hooks support."""
from typing import Optional, Any
from .config import Config
from ..middleware.base import MiddlewareChain, Context
from ..hooks.manager import HookManager, HookType

class Application:
    """Main application class."""
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self.middleware = MiddlewareChain(self.config)
        self.hooks = HookManager()
    
    async def process_request(self, request: Any) -> Any:
        """Process request through middleware chain and hooks."""
        # Trigger before request hooks
        request = await self.hooks.trigger(HookType.BEFORE_REQUEST, request)
        
        # Create context
        context = Context(request=request)
        
        try:
            # Execute middleware chain
            context = await self.middleware.execute(context)
            
            # Trigger after request hooks
            context.response = await self.hooks.trigger(
                HookType.AFTER_REQUEST,
                context.response
            )
            
            # Trigger success hooks
            await self.hooks.trigger(HookType.ON_SUCCESS, context)
            
            return context.response
            
        except Exception as e:
            # Trigger error hooks
            await self.hooks.trigger(HookType.ON_ERROR, e)
            raise 