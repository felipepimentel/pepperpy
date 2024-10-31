from pepperpy.core.application import Application
from pepperpy.middleware.base import LoggingMiddleware, CacheMiddleware
from pepperpy.hooks.manager import HookType

async def demonstrate_middleware_hooks():
    app = Application()
    
    # Adicionar middleware
    app.middleware.use(LoggingMiddleware())
    app.middleware.use(CacheMiddleware())
    
    # Registrar hooks
    @app.hooks.before_request()
    async def validate_request(context):
        print("Validating request...")
        return context
    
    @app.hooks.on_error()
    async def handle_error(error):
        print(f"Error handled: {error}")
    
    # Processar request
    response = await app.process_request({"action": "get_data"})
    print(f"Response: {response}") 