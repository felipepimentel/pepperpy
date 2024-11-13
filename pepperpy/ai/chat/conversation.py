"""Conversation builder implementation"""

from typing import AsyncIterator, List, Optional, Union

from ..client import AIClient, AIResponse
from ..exceptions import AIError
from .types import ChatMessage, ChatRole


class Conversation:
    """Builder for creating and managing AI conversations

    Example:
        ```python
        async with AIClient.create() as client:
            response = await (
                Conversation()
                .system("You are a Python expert.")
                .user("How do I use async/await?")
                .complete(client)
            )
        ```
    """

    def __init__(self) -> None:
        """Initialize an empty conversation"""
        self._messages: List[ChatMessage] = []

    @property
    def messages(self) -> List[ChatMessage]:
        """Get all messages in the conversation"""
        return self._messages.copy()

    def add_message(
        self, role: ChatRole, content: str, name: Optional[str] = None
    ) -> "Conversation":
        """Add a message to the conversation

        Args:
            role: The role of the message sender
            content: The message content
            name: Optional name for the message sender

        Returns:
            self: For method chaining
        """
        self._messages.append(ChatMessage(role=role, content=content, name=name))
        return self

    def system(self, content: str) -> "Conversation":
        """Add a system message

        Args:
            content: The system instruction

        Returns:
            self: For method chaining
        """
        return self.add_message("system", content)

    def user(self, content: str, name: Optional[str] = None) -> "Conversation":
        """Add a user message

        Args:
            content: The user's message
            name: Optional name for the user

        Returns:
            self: For method chaining
        """
        return self.add_message("user", content, name)

    def assistant(self, content: str, name: Optional[str] = None) -> "Conversation":
        """Add an assistant message

        Args:
            content: The assistant's message
            name: Optional name for the assistant

        Returns:
            self: For method chaining
        """
        return self.add_message("assistant", content, name)

    def clear(self) -> "Conversation":
        """Clear all messages from the conversation

        Returns:
            self: For method chaining
        """
        self._messages.clear()
        return self

    async def complete(self, client: AIClient) -> AIResponse:
        """Complete the conversation using the provided AI client

        Args:
            client: The AI client to use

        Returns:
            AIResponse: The AI's response

        Raises:
            AIError: If the conversation is empty or completion fails
        """
        if not self._messages:
            raise AIError("Cannot complete empty conversation")

        try:
            # Convert ChatMessage to dict format expected by client
            messages = [{"role": msg.role, "content": msg.content} for msg in self._messages]
            return await client.complete(messages)
        except Exception as e:
            raise AIError("Failed to complete conversation", cause=e)

    async def stream(self, client: AIClient) -> AsyncIterator[AIResponse]:
        """Stream the conversation completion using the provided AI client

        Args:
            client: The AI client to use

        Yields:
            AIResponse: The AI's response chunks

        Raises:
            AIError: If the conversation is empty or streaming fails
        """
        if not self._messages:
            raise AIError("Cannot stream empty conversation")

        try:
            messages = [{"role": msg.role, "content": msg.content} for msg in self._messages]
            async for response in client.stream(messages):
                yield response
        except Exception as e:
            raise AIError("Failed to stream conversation", cause=e)

    @classmethod
    def from_messages(cls, messages: List[Union[ChatMessage, dict]]) -> "Conversation":
        """Create a conversation from a list of messages

        Args:
            messages: List of ChatMessage objects or dicts with role and content

        Returns:
            Conversation: New conversation with the provided messages

        Raises:
            AIError: If message format is invalid
        """
        conversation = cls()

        for msg in messages:
            if isinstance(msg, ChatMessage):
                conversation._messages.append(msg)
            elif isinstance(msg, dict):
                if "role" not in msg or "content" not in msg:
                    raise AIError("Message dict must contain 'role' and 'content' keys")
                conversation.add_message(
                    role=msg["role"], content=msg["content"], name=msg.get("name")
                )
            else:
                raise AIError(f"Invalid message type: {type(msg)}")

        return conversation
