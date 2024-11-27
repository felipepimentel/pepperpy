"""Chat conversation implementation"""

from typing import Any

from bko.ai.chat.types import ChatHistory, ChatMessage, ChatMetadata, ChatRole
from bko.ai.providers.base import AIProvider as BaseAIProvider
from bko.ai.types import AIResponse
from bko.core.exceptions import PepperPyError


class Conversation:
    """Chat conversation manager"""

    def __init__(self, client: BaseAIProvider, metadata: ChatMetadata) -> None:
        """Initialize conversation.

        Args:
            client: AI client
            metadata: Chat metadata
        """
        self._client = client
        self._metadata = metadata
        self._history = ChatHistory(
            messages=[],
            metadata={
                "session_id": metadata.session_id,
                "user_id": metadata.user_id,
                "context": metadata.context,
                "settings": metadata.settings,
            },
        )
        self._initialized = False

    @property
    def is_initialized(self) -> bool:
        """Check if conversation is initialized"""
        return self._initialized

    @property
    def history(self) -> ChatHistory:
        """Get conversation history"""
        return self._history

    async def initialize(self) -> None:
        """Initialize conversation"""
        if not self._client.is_initialized:
            await self._client.initialize()
        self._initialized = True

    async def cleanup(self) -> None:
        """Cleanup conversation resources"""
        if self._client.is_initialized:
            await self._client.cleanup()
        self._initialized = False

    def add_message(self, message: ChatMessage) -> None:
        """Add message to history.

        Args:
            message: Message to add
        """
        self._history.add_message(message)

    def clear_history(self) -> None:
        """Clear conversation history"""
        self._history.clear()

    def get_history(self) -> ChatHistory:
        """Get conversation history.

        Returns:
            ChatHistory: Current conversation history
        """
        return self._history

    async def send(self, message: str, **kwargs: Any) -> AIResponse:
        """Send message and get response.

        Args:
            message: Message content
            **kwargs: Additional arguments for completion

        Returns:
            AIResponse: AI response

        Raises:
            PepperPyError: If sending fails
            RuntimeError: If conversation is not initialized
        """
        if not self._initialized:
            raise RuntimeError("Conversation is not initialized")

        # Add user message to history
        user_message = ChatMessage(
            role=ChatRole.USER, content=message, metadata=kwargs.get("metadata", {})
        )
        self.add_message(user_message)

        try:
            # Get AI response
            response = await self._client.complete(message, **kwargs)

            # Add assistant message to history
            assistant_message = ChatMessage(
                role=ChatRole.ASSISTANT, content=response.content, metadata=response.metadata
            )
            self.add_message(assistant_message)

            return response
        except Exception as e:
            raise PepperPyError(f"Failed to send message: {e}", cause=e)
