"""Example of WebSocket functionality."""
import asyncio
from pepperpy.websocket import (
    WebSocketServer,
    WebSocketClient,
    WebSocketHandler,
    WebSocketMessage,
    WebSocketConfig
)

class ChatHandler(WebSocketHandler):
    """Example chat handler."""
    
    async def handle_message(self, message: WebSocketMessage, send: callable) -> None:
        """Handle chat messages."""
        if message.type == "chat":
            # Echo message back to sender
            await send({
                "type": "chat",
                "data": {
                    "message": f"Echo: {message.data.get('message', '')}"
                }
            })
    
    async def handle_connect(self, client_id: str) -> None:
        """Handle client connection."""
        print(f"Client {client_id} connected")
    
    async def handle_disconnect(self, client_id: str) -> None:
        """Handle client disconnection."""
        print(f"Client {client_id} disconnected")

async def run_server():
    """Run WebSocket server."""
    config = WebSocketConfig(
        host="localhost",
        port=8765
    )
    
    server = WebSocketServer(
        ChatHandler(),
        config
    )
    
    await server.start()
    
    try:
        while True:
            # Broadcast message every 5 seconds
            await server.broadcast({
                "type": "announcement",
                "data": {
                    "message": "Server is running!"
                }
            })
            await asyncio.sleep(5)
    finally:
        await server.stop()

async def run_client():
    """Run WebSocket client."""
    client = WebSocketClient(
        "ws://localhost:8765",
        ChatHandler()
    )
    
    await client.connect()
    
    try:
        # Send message every 2 seconds
        while True:
            await client.send({
                "type": "chat",
                "data": {
                    "message": "Hello, server!"
                }
            })
            await asyncio.sleep(2)
    finally:
        await client.disconnect()

async def demonstrate_websocket():
    """Demonstrate WebSocket functionality."""
    # Start server in background
    server_task = asyncio.create_task(run_server())
    
    # Wait for server to start
    await asyncio.sleep(1)
    
    # Start multiple clients
    client_tasks = [
        asyncio.create_task(run_client())
        for _ in range(3)
    ]
    
    # Run for 30 seconds
    await asyncio.sleep(30)
    
    # Cancel all tasks
    for task in client_tasks:
        task.cancel()
    server_task.cancel()
    
    # Wait for tasks to finish
    await asyncio.gather(
        *client_tasks,
        server_task,
        return_exceptions=True
    )

if __name__ == "__main__":
    asyncio.run(demonstrate_websocket()) 