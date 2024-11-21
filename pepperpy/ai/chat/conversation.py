"""Chat conversation implementation"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Sequence

from pepperpy.core.module import InitializableModule

from ..types import AIMessage, AIResponse, MessageRole


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


class ConversationManager(InitializableModule):
    """Chat conversation manager"""

    def __init__(self) -> None:
        super().__init__()
        self._conversations: dict[str, Conversation] = {}

    async def _initialize(self) -> None:
        """Initialize conversation manager"""
        pass

    async def _cleanup(self) -> None:
        """Cleanup conversation manager"""
        self._conversations.clear()

    async def create(self, id_: str | None = None) -> Conversation:
        """Create new conversation"""
        self._ensure_initialized()
        conv_id = id_ or self._generate_id()
        conversation = Conversation(id=conv_id)
        self._conversations[conv_id] = conversation
        return conversation

    async def process_message(self, conversation: Conversation, message: str) -> AIResponse:
        """Process message in conversation"""
        self._ensure_initialized()
        try:
            response = await self._generate_response(message)
            await conversation.add_message(AIMessage(role=MessageRole.USER, content=message))
            await conversation.add_message(AIMessage(role=MessageRole.ASSISTANT, content=response))
            return AIResponse(
                content=response,
                messages=conversation.messages,
            )
        except Exception as e:
            raise ValueError(f"Failed to process message: {e}")

    async def _generate_response(self, message: str) -> str:
        """Generate response for message"""
        # Implementar geração real de resposta
        return f"Echo: {message}"

    def _generate_id(self) -> str:
        """Generate unique conversation ID"""
        return datetime.now().strftime("%Y%m%d%H%M%S")
