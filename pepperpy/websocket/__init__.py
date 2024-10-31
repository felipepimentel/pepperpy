"""WebSocket module for real-time communication."""
from typing import Optional, Dict, Any, Callable, List, Union
from dataclasses import dataclass, field
import asyncio
import json
from abc import ABC, abstractmethod
from datetime import datetime
import websockets
from loguru import logger

@dataclass
class WebSocketConfig:
    """Configuration for WebSocket connections."""
    host: str = "0.0.0.0"
    port: int = 8765
    ping_interval: float = 20.0
    ping_timeout: float = 10.0
    max_size: int = 10 * 1024 * 1024  # 10MB
    max_connections: int = 1000
    ssl_context: Optional[Any] = None

@dataclass
class WebSocketMessage:
    """Represents a WebSocket message."""
    type: str
    data: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)
    sender: Optional[str] = None

class WebSocketHandler(ABC):
    """Base class for WebSocket message handlers."""
    
    @abstractmethod
    async def handle_message(
        self,
        message: WebSocketMessage,
        send: Callable
    ) -> None:
        """Handle incoming message."""
        pass
    
    @abstractmethod
    async def handle_connect(self, client_id: str) -> None:
        """Handle client connection."""
        pass
    
    @abstractmethod
    async def handle_disconnect(self, client_id: str) -> None:
        """Handle client disconnection."""
        pass

class WebSocketServer:
    """WebSocket server implementation."""
    
    def __init__(
        self,
        handler: WebSocketHandler,
        config: Optional[WebSocketConfig] = None
    ):
        self.handler = handler
        self.config = config or WebSocketConfig()
        self.clients: Dict[str, websockets.WebSocketServerProtocol] = {}
        self._server: Optional[websockets.WebSocketServer] = None
        self._running = False
    
    async def start(self) -> None:
        """Start the WebSocket server."""
        self._running = True
        self._server = await websockets.serve(
            self._handle_client,
            self.config.host,
            self.config.port,
            ping_interval=self.config.ping_interval,
            ping_timeout=self.config.ping_timeout,
            max_size=self.config.max_size,
            ssl=self.config.ssl_context
        )
        
        logger.info(
            f"WebSocket server started on ws://{self.config.host}:{self.config.port}"
        )
    
    async def stop(self) -> None:
        """Stop the WebSocket server."""
        self._running = False
        if self._server:
            self._server.close()
            await self._server.wait_closed()
            self._server = None
        
        # Disconnect all clients
        for client_id in list(self.clients.keys()):
            await self._handle_disconnect(client_id)
    
    async def broadcast(
        self,
        message: Union[str, Dict, WebSocketMessage],
        exclude: Optional[List[str]] = None
    ) -> None:
        """Broadcast message to all connected clients."""
        if isinstance(message, (str, dict)):
            message = WebSocketMessage(
                type="broadcast",
                data=message if isinstance(message, dict) else {"message": message}
            )
        
        message_data = {
            "type": message.type,
            "data": message.data,
            "timestamp": message.timestamp.isoformat(),
            "sender": message.sender
        }
        
        exclude_set = set(exclude or [])
        tasks = []
        
        for client_id, websocket in self.clients.items():
            if client_id not in exclude_set:
                tasks.append(
                    websocket.send(json.dumps(message_data))
                )
        
        if tasks:
            await asyncio.gather(*tasks)
    
    async def send_to(
        self,
        client_id: str,
        message: Union[str, Dict, WebSocketMessage]
    ) -> None:
        """Send message to specific client."""
        if client_id not in self.clients:
            raise ValueError(f"Client not found: {client_id}")
            
        if isinstance(message, (str, dict)):
            message = WebSocketMessage(
                type="direct",
                data=message if isinstance(message, dict) else {"message": message}
            )
        
        message_data = {
            "type": message.type,
            "data": message.data,
            "timestamp": message.timestamp.isoformat(),
            "sender": message.sender
        }
        
        await self.clients[client_id].send(json.dumps(message_data))
    
    async def _handle_client(
        self,
        websocket: websockets.WebSocketServerProtocol,
        path: str
    ) -> None:
        """Handle client connection and messages."""
        if len(self.clients) >= self.config.max_connections:
            await websocket.close(1013, "Maximum connections reached")
            return
        
        client_id = str(id(websocket))
        self.clients[client_id] = websocket
        
        try:
            await self.handler.handle_connect(client_id)
            
            async for message in websocket:
                try:
                    data = json.loads(message)
                    ws_message = WebSocketMessage(
                        type=data.get("type", "message"),
                        data=data.get("data", {}),
                        sender=client_id
                    )
                    
                    await self.handler.handle_message(
                        ws_message,
                        lambda msg: self.send_to(client_id, msg)
                    )
                    
                except json.JSONDecodeError:
                    logger.warning(f"Invalid JSON from client {client_id}")
                    
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"Client {client_id} connection closed")
            
        finally:
            await self._handle_disconnect(client_id)
    
    async def _handle_disconnect(self, client_id: str) -> None:
        """Handle client disconnection."""
        if client_id in self.clients:
            await self.clients[client_id].close()
            del self.clients[client_id]
            await self.handler.handle_disconnect(client_id)

class WebSocketClient:
    """WebSocket client implementation."""
    
    def __init__(
        self,
        url: str,
        handler: WebSocketHandler,
        ssl_context: Optional[Any] = None
    ):
        self.url = url
        self.handler = handler
        self.ssl_context = ssl_context
        self._websocket: Optional[websockets.WebSocketClientProtocol] = None
        self._running = False
    
    async def connect(self) -> None:
        """Connect to WebSocket server."""
        self._running = True
        self._websocket = await websockets.connect(
            self.url,
            ssl=self.ssl_context
        )
        
        await self.handler.handle_connect(str(id(self._websocket)))
        
        try:
            async for message in self._websocket:
                try:
                    data = json.loads(message)
                    ws_message = WebSocketMessage(
                        type=data.get("type", "message"),
                        data=data.get("data", {}),
                        sender=data.get("sender")
                    )
                    
                    await self.handler.handle_message(
                        ws_message,
                        self.send
                    )
                    
                except json.JSONDecodeError:
                    logger.warning("Invalid JSON received")
                    
        except websockets.exceptions.ConnectionClosed:
            logger.info("Connection closed")
            
        finally:
            await self.disconnect()
    
    async def disconnect(self) -> None:
        """Disconnect from WebSocket server."""
        self._running = False
        if self._websocket:
            await self._websocket.close()
            await self.handler.handle_disconnect(str(id(self._websocket)))
            self._websocket = None
    
    async def send(
        self,
        message: Union[str, Dict, WebSocketMessage]
    ) -> None:
        """Send message to server."""
        if not self._websocket:
            raise RuntimeError("Not connected to server")
            
        if isinstance(message, (str, dict)):
            message = WebSocketMessage(
                type="message",
                data=message if isinstance(message, dict) else {"message": message}
            )
        
        message_data = {
            "type": message.type,
            "data": message.data,
            "timestamp": message.timestamp.isoformat()
        }
        
        await self._websocket.send(json.dumps(message_data)) 