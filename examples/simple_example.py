from pepperpy import Pepperpy
from pepperpy.decorators import cached, retry

async def main():
    # Inicialização simples
    app = Pepperpy()
    
    # Cache automático
    @app.cache.cached(ttl=300)
    async def get_data():
        return await app.http.get("https://api.exemplo.com/data")
    
    # Retry automático
    @app.retry(attempts=3)
    async def process_data():
        data = await get_data()
        return await app.llm.process(data)
    
    # Eventos
    @app.events.on("data.processed")
    async def handle_processed(result):
        await app.db.save(result)
    
    result = await process_data()
    await app.events.emit("data.processed", result) 