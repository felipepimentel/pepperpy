"""Tests for chat conversation"""

from unittest.mock import AsyncMock

import pytest

from pepperpy.ai.chat.conversation import Conversation
from pepperpy.ai.chat.types import ChatHistory, ChatMessage, ChatMetadata, ChatRole
from pepperpy.ai.types import AIMessage, AIResponse, MessageRole
from pepperpy.core.exceptions import PepperPyError


@pytest.fixture
def mock_ai_client():
    """Fixture for mock AI client"""
    client = AsyncMock()
    client.is_initialized = False
    client.initialize = AsyncMock()
    client.cleanup = AsyncMock()
    client.complete = AsyncMock(return_value=AIResponse(
        content="Hello!",
        messages=[AIMessage(role=MessageRole.ASSISTANT, content="Hello!")],
        metadata={}
    ))
    return client


@pytest.fixture
def chat_metadata():
    """Fixture for chat metadata"""
    return ChatMetadata(
        session_id="test-session",
        user_id="test-user",
        context={"language": "en"},
        settings={"temperature": 0.7}
    )


@pytest.mark.asyncio
async def test_conversation_initialization(mock_ai_client, chat_metadata):
    """Test conversation initialization"""
    conversation = Conversation(mock_ai_client, chat_metadata)
    assert not conversation.is_initialized
    await conversation.initialize()
    assert conversation.is_initialized
    mock_ai_client.initialize.assert_called_once()


@pytest.mark.asyncio
async def test_conversation_cleanup(mock_ai_client, chat_metadata):
    """Test conversation cleanup"""
    conversation = Conversation(mock_ai_client, chat_metadata)
    await conversation.initialize()
    mock_ai_client.is_initialized = True  # Set client as initialized
    await conversation.cleanup()
    
    assert not conversation.is_initialized
    mock_ai_client.cleanup.assert_called_once()


def test_conversation_add_message(mock_ai_client, chat_metadata):
    """Test adding message to conversation"""
    conversation = Conversation(mock_ai_client, chat_metadata)
    message = ChatMessage(role=ChatRole.USER, content="Hello")
    
    conversation.add_message(message)
    
    assert len(conversation.history.messages) == 1
    assert conversation.history.messages[0] == message


def test_conversation_clear_history(mock_ai_client, chat_metadata):
    """Test clearing conversation history"""
    conversation = Conversation(mock_ai_client, chat_metadata)
    message = ChatMessage(role=ChatRole.USER, content="Hello")
    
    conversation.add_message(message)
    conversation.clear_history()
    
    assert len(conversation.history.messages) == 0


def test_conversation_get_history(mock_ai_client, chat_metadata):
    """Test getting conversation history"""
    conversation = Conversation(mock_ai_client, chat_metadata)
    message = ChatMessage(role=ChatRole.USER, content="Hello")
    
    conversation.add_message(message)
    history = conversation.get_history()
    
    assert isinstance(history, ChatHistory)
    assert len(history.messages) == 1
    assert history.messages[0] == message
    assert history.metadata == {
        "session_id": chat_metadata.session_id,
        "user_id": chat_metadata.user_id,
        "context": chat_metadata.context,
        "settings": chat_metadata.settings
    }


@pytest.mark.asyncio
async def test_conversation_send_message(mock_ai_client, chat_metadata):
    """Test sending message in conversation"""
    conversation = Conversation(mock_ai_client, chat_metadata)
    await conversation.initialize()
    
    response = await conversation.send("Hello", metadata={"timestamp": "2024-01-01"})
    
    assert response.content == "Hello!"
    assert len(conversation.history.messages) == 2  # User message + Assistant response
    assert conversation.history.messages[0].role == ChatRole.USER
    assert conversation.history.messages[0].content == "Hello"
    assert conversation.history.messages[1].role == ChatRole.ASSISTANT
    assert conversation.history.messages[1].content == "Hello!"


@pytest.mark.asyncio
async def test_conversation_send_not_initialized(mock_ai_client, chat_metadata):
    """Test sending message when not initialized"""
    conversation = Conversation(mock_ai_client, chat_metadata)
    
    with pytest.raises(RuntimeError, match="not initialized"):
        await conversation.send("Hello")


@pytest.mark.asyncio
async def test_conversation_send_error(mock_ai_client, chat_metadata):
    """Test sending message with error"""
    conversation = Conversation(mock_ai_client, chat_metadata)
    await conversation.initialize()
    
    mock_ai_client.complete.side_effect = Exception("Failed to send")
    
    with pytest.raises(PepperPyError, match="Failed to send message"):
        await conversation.send("Hello")


def test_conversation_history_property(mock_ai_client, chat_metadata):
    """Test conversation history property"""
    conversation = Conversation(mock_ai_client, chat_metadata)
    history = conversation.history
    
    assert isinstance(history, ChatHistory)
    assert history.metadata == {
        "session_id": chat_metadata.session_id,
        "user_id": chat_metadata.user_id,
        "context": chat_metadata.context,
        "settings": chat_metadata.settings
    }


def test_conversation_is_initialized_property(mock_ai_client, chat_metadata):
    """Test conversation is_initialized property"""
    conversation = Conversation(mock_ai_client, chat_metadata)
    assert not conversation.is_initialized
    