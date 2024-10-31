"""Example of infrastructure features."""
import asyncio
from pepperpy.cache import DistributedCache
from pepperpy.queue import JobWorker
from pepperpy.metrics import MetricsCollector

async def demonstrate_infrastructure():
    # Cache distribuído
    cache = DistributedCache()
    await cache.set("user:1", {"name": "John", "age": 30})
    user = await cache.get("user:1")
    
    # Sistema de filas
    worker = JobWorker()
    
    @worker.register_handler("email")
    async def send_email(payload):
        print(f"Sending email to {payload['to']}")
    
    # Métricas
    metrics = MetricsCollector()
    
    # Medindo tempo de operação
    complete_timing = metrics.measure_time(
        "api_request",
        {"method": "GET", "endpoint": "/users"}
    )
    
    try:
        # Simular operação
        await asyncio.sleep(1)
        complete_timing()
    except Exception as e:
        metrics.count_error("api_error")

if __name__ == "__main__":
    asyncio.run(demonstrate_infrastructure()) 