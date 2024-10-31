"""Conversation memory management."""
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Message:
    """Single conversation message."""
    role: str
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

class ConversationMemory:
    """Manages conversation history and context."""
    
    def __init__(
        self,
        max_messages: Optional[int] = None,
        include_timestamps: bool = True
    ):
        self.messages: List[Message] = []
        self.max_messages = max_messages
        self.include_timestamps = include_timestamps
        
    def add_message(
        self,
        role: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Add a message to the conversation."""
        message = Message(
            role=role,
            content=content,
            metadata=metadata or {}
        )
        
        self.messages.append(message)
        
        if self.max_messages and len(self.messages) > self.max_messages:
            self.messages.pop(0)
            
    def get_context(
        self,
        include_metadata: bool = False
    ) -> List[Dict[str, str]]:
        """Get conversation context for LLM."""
        return [
            {
                "role": msg.role,
                "content": msg.content,
                **({"metadata": msg.metadata} if include_metadata else {})
            }
            for msg in self.messages
        ]
        
    def clear(self) -> None:
        """Clear conversation history."""
        self.messages.clear() 