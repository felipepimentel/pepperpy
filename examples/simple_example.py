from pepperpy import Pepperpy
import asyncio

async def main():
    # Inicialização simples
    app = Pepperpy()
    
    # Ou com configuração via arquivo
    # app = Pepperpy.from_file("config.yml")
    
    # Context manager cuida da inicialização/finalização
    async with app as pepperpy:
        # Logging elegante
        pepperpy.log.info("Aplicação iniciada")
        
        # HTTP simplificado
        users = await pepperpy.http.get("https://api.exemplo.com/users")
        pepperpy.log.info(f"Usuários: {users}")
        
        # Banco de dados com context manager
        async with pepperpy.db.session() as session:
            await session.execute(
                "CREATE TABLE IF NOT EXISTS users (id INT, name TEXT)"
            )
            
            await session.execute(
                "INSERT INTO users VALUES (?, ?)",
                [(1, "João"), (2, "Maria")]
            )
            
            results = await session.fetch("SELECT * FROM users")
            pepperpy.log.info(f"Usuários no banco: {results}")
        
        # Cache automático
        @pepperpy.cache.cached(ttl=300)
        async def get_data():
            return await pepperpy.http.get("https://api.exemplo.com/data")
        
        data = await get_data()
        
        # IA/LLM
        response = await pepperpy.ai.ask(
            "Como implementar cache em Python?",
            model="gpt-4"
        )
        
        # Eventos
        @pepperpy.events.on("user.created")
        async def handle_user_created(user):
            pepperpy.log.info(f"Novo usuário: {user}")
        
        await pepperpy.events.emit("user.created", {"id": 1, "name": "João"})
        
        # Mensageria
        await pepperpy.broker.publish(
            "notifications",
            {"type": "welcome", "user_id": 1}
        )

if __name__ == "__main__":
    asyncio.run(main()) 