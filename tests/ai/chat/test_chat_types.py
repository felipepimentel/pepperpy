"""Tests for chat types"""


import pytest

from pepperpy.ai.chat.types import ChatHistory, ChatMessage, ChatMetadata, ChatRole


def test_chat_message_creation():
    """Test chat message creation"""
    message = ChatMessage(
        role=ChatRole.USER,
        content="Hello, how are you?",
        metadata={"timestamp": "2024-01-01"}
    )
    
    assert message.role == ChatRole.USER
    assert message.content == "Hello, how are you?"
    assert message.metadata == {"timestamp": "2024-01-01"}


def test_chat_message_default_metadata():
    """Test chat message default metadata"""
    message = ChatMessage(
        role=ChatRole.ASSISTANT,
        content="I'm doing well, thanks!"
    )
    
    assert message.metadata == {}


def test_chat_message_validation():
    """Test chat message validation"""
    with pytest.raises(ValueError, match="Content cannot be empty"):
        ChatMessage(
            role=ChatRole.USER,
            content=""  # Empty content should raise error
        )


def test_chat_history_creation():
    """Test chat history creation"""
    messages = [
        ChatMessage(role=ChatRole.USER, content="Hello"),
        ChatMessage(role=ChatRole.ASSISTANT, content="Hi there!")
    ]
    
    history = ChatHistory(
        messages=messages,
        metadata={"session_id": "123"}
    )
    
    assert history.messages == messages
    assert history.metadata == {"session_id": "123"}


def test_chat_history_default_values():
    """Test chat history default values"""
    history = ChatHistory()
    
    assert history.messages == []
    assert history.metadata == {}


def test_chat_history_add_message():
    """Test adding message to chat history"""
    history = ChatHistory()
    message = ChatMessage(role=ChatRole.USER, content="Hello")
    
    history.add_message(message)
    
    assert len(history.messages) == 1
    assert history.messages[0] == message


def test_chat_history_clear():
    """Test clearing chat history"""
    history = ChatHistory(messages=[
        ChatMessage(role=ChatRole.USER, content="Hello"),
        ChatMessage(role=ChatRole.ASSISTANT, content="Hi!")
    ])
    
    history.clear()
    
    assert len(history.messages) == 0


def test_chat_metadata_creation():
    """Test chat metadata creation"""
    metadata = ChatMetadata(
        session_id="123",
        user_id="user123",
        context={"language": "en"},
        settings={"temperature": 0.7}
    )
    
    assert metadata.session_id == "123"
    assert metadata.user_id == "user123"
    assert metadata.context == {"language": "en"}
    assert metadata.settings == {"temperature": 0.7}


def test_chat_metadata_default_values():
    """Test chat metadata default values"""
    metadata = ChatMetadata(
        session_id="123",
        user_id="user123"
    )
    
    assert metadata.context == {}
    assert metadata.settings == {}


def test_chat_metadata_validation():
    """Test chat metadata validation"""
    with pytest.raises(ValueError, match="Session ID cannot be empty"):
        ChatMetadata(
            session_id="",  # Empty session_id should raise error
            user_id="user123"
        )

    with pytest.raises(ValueError, match="User ID cannot be empty"):
        ChatMetadata(
            session_id="123",
            user_id=""  # Empty user_id should raise error
        )


def test_chat_role_values():
    """Test chat role enumeration values"""
    assert ChatRole.USER.value == "user"
    assert ChatRole.ASSISTANT.value == "assistant"
    assert ChatRole.SYSTEM.value == "system"
    assert ChatRole.FUNCTION.value == "function"


def test_chat_role_comparison():
    """Test chat role comparison"""
    assert ChatRole.USER == ChatRole.USER
    assert ChatRole.USER != ChatRole.ASSISTANT
    assert ChatRole.USER.value == "user"


def test_chat_message_string_representation():
    """Test chat message string representation"""
    message = ChatMessage(
        role=ChatRole.USER,
        content="Hello",
        metadata={"timestamp": "2024-01-01"}
    )
    
    expected_str = (
        "ChatMessage(role=user, content=Hello, "
        "metadata={'timestamp': '2024-01-01'})"
    )
    assert str(message) == expected_str


def test_chat_history_string_representation():
    """Test chat history string representation"""
    history = ChatHistory(
        messages=[
            ChatMessage(role=ChatRole.USER, content="Hello", metadata={}),
            ChatMessage(role=ChatRole.ASSISTANT, content="Hi!", metadata={})
        ],
        metadata={"session_id": "123"}
    )
    
    # Get actual string representation
    actual_str = str(history)
    
    # Verify each component separately for better error messages
    assert "ChatHistory(messages=[" in actual_str
    assert "ChatMessage(role=user, content=Hello, metadata={})" in actual_str
    assert "ChatMessage(role=assistant, content=Hi!, metadata={})" in actual_str
    assert "metadata={'session_id': '123'}" in actual_str


def test_chat_metadata_string_representation():
    """Test chat metadata string representation"""
    metadata = ChatMetadata(
        session_id="123",
        user_id="user123",
        context={"language": "en"},
        settings={"temperature": 0.7}
    )
    
    expected_str = (
        "ChatMetadata(session_id=123, user_id=user123, "
        "context={'language': 'en'}, settings={'temperature': 0.7})"
    )
    assert str(metadata) == expected_str
    