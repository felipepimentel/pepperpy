"""Chat conversation implementation"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Sequence

from pepperpy.core.module import BaseModule

from ..types import AIMessage, AIResponse


@dataclass
class Conversation:
    """Chat conversation"""

    id: str
    messages: list[AIMessage] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    async def add_message(self, message: AIMessage) -> None:
        """Add message to conversation"""
        self.messages.append(message)
        self.updated_at = datetime.now()

    async def get_messages(self) -> Sequence[AIMessage]:
        """Get conversation messages"""
        return self.messages

    async def clear(self) -> None:
        """Clear conversation messages"""
        self.messages.clear()
        self.updated_at = datetime.now()


class ConversationManager(BaseModule):
    """Chat conversation manager"""

    async def create(self, id_: str | None = None) -> Conversation:
        """Create new conversation"""
        conv_id = id_ or self._generate_id()
        return Conversation(id=conv_id)

    async def process_message(self, conversation: Conversation, message: str) -> AIResponse:
        """Process message in conversation"""
        try:
            # Implementar processamento real da mensagem
            response = await self._generate_response(message)
            await conversation.add_message(AIMessage(role="user", content=message))
            await conversation.add_message(AIMessage(role="assistant", content=response))
            return AIResponse(content=response)
        except Exception as e:
            raise ValueError(f"Failed to process message: {e}")

    async def _generate_response(self, message: str) -> str:
        """Generate response for message"""
        # Implementar geração real de resposta
        return f"Echo: {message}"

    def _generate_id(self) -> str:
        """Generate unique conversation ID"""
        return datetime.now().strftime("%Y%m%d%H%M%S")
