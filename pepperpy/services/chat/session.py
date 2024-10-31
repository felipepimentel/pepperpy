"""Chat session management."""
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime

from ...llm.base import BaseLLM
from ...llm.types import Message
from .memory import ChatMemory

@dataclass
class ChatSession:
    """Manages a chat session with memory and state."""
    
    def __init__(
        self,
        llm: BaseLLM,
        memory: Optional[ChatMemory] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.llm = llm
        self.memory = memory or ChatMemory()
        self.metadata = metadata or {}
        self.created_at = datetime.now()
        self.last_activity = self.created_at
        
    async def send_message(
        self,
        content: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Send a message and get response."""
        self.last_activity = datetime.now()
        
        # Get conversation context
        messages = self.memory.get_context()
        messages.append({"role": "user", "content": content})
        
        # Get response
        response = await self.llm.achat(messages, **kwargs)
        
        # Update memory
        self.memory.add_message("user", content)
        self.memory.add_message("assistant", response.content)
        
        return {
            "content": response.content,
            "usage": response.usage,
            "cost": response.cost,
            "metadata": {
                **response.metadata,
                "session_id": id(self),
                "timestamp": self.last_activity.isoformat()
            }
        } 