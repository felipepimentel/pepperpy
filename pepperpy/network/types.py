"""Network type definitions"""

import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from aiohttp import ClientWebSocketResponse


@dataclass
class Request:
    """HTTP request information"""

    method: str
    url: str
    headers: Dict[str, str]
    params: Dict[str, str]
    data: Any
    timeout: float


@dataclass
class Response:
    """HTTP response information"""

    status: int
    headers: Dict[str, str]
    content: bytes
    text: str
    json: Optional[Dict[str, Any]]
    elapsed: float


@dataclass
class WebSocket:
    """WebSocket connection"""

    url: str
    connection: ClientWebSocketResponse
    protocols: List[str]

    async def send(self, data: Any) -> None:
        """Send data through WebSocket"""
        await self.connection.send_str(json.dumps(data))

    async def receive(self) -> Any:
        """Receive data from WebSocket"""
        msg = await self.connection.receive_str()
        return json.loads(msg)

    async def close(self) -> None:
        """Close WebSocket connection"""
        await self.connection.close()
