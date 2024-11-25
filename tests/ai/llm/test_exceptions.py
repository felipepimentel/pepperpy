"""Tests for LLM exceptions module"""

import pytest

from pepperpy.ai.llm.exceptions import (
    AuthenticationError,
    LLMError,
    ModelNotFoundError,
    PromptError,
    RateLimitError,
    ResponseError,
    TokenLimitError,
)


def test_llm_error_basic():
    """Test basic LLM error creation"""
    error = LLMError("Test error")
    assert str(error) == "Test error"
    assert error.message == "Test error"
    assert error.cause is None


def test_llm_error_with_cause():
    """Test LLM error with cause"""
    cause = ValueError("Original error")
    error = LLMError("Test error", cause=cause)
    assert str(error) == "Test error"
    assert error.message == "Test error"
    assert error.cause == cause


def test_model_not_found_error():
    """Test model not found error"""
    error = ModelNotFoundError("gpt-5")
    assert "gpt-5" in str(error)
    assert isinstance(error, LLMError)


def test_token_limit_error():
    """Test token limit error"""
    error = TokenLimitError(max_tokens=4096, actual_tokens=5000)
    assert "4096" in str(error)
    assert "5000" in str(error)
    assert isinstance(error, LLMError)


def test_prompt_error():
    """Test prompt error"""
    error = PromptError("Invalid prompt format")
    assert "Invalid prompt format" in str(error)
    assert isinstance(error, LLMError)


def test_response_error():
    """Test response error"""
    error = ResponseError("Invalid response format")
    assert "Invalid response format" in str(error)
    assert isinstance(error, LLMError)


def test_rate_limit_error():
    """Test rate limit error"""
    error = RateLimitError("Too many requests")
    assert "Too many requests" in str(error)
    assert isinstance(error, LLMError)


def test_authentication_error():
    """Test authentication error"""
    error = AuthenticationError("Invalid API key")
    assert "Invalid API key" in str(error)
    assert isinstance(error, LLMError)


def test_llm_error_inheritance_chain():
    """Test LLM error inheritance chain"""
    errors = [
        ModelNotFoundError("test"),
        TokenLimitError(1000, 2000),
        PromptError("test"),
        ResponseError("test"),
        RateLimitError("test"),
        AuthenticationError("test"),
    ]

    for error in errors:
        assert isinstance(error, LLMError)
        assert isinstance(error, Exception)


def test_llm_error_with_empty_message():
    """Test LLM error with empty message"""
    error = LLMError("")
    assert str(error) == ""
    assert error.message == ""
    assert error.cause is None


def test_llm_error_with_none_message():
    """Test LLM error with None message"""
    with pytest.raises(ValueError) as exc_info:
        LLMError(None)  # type: ignore
    assert "Message cannot be None" in str(exc_info.value)


def test_token_limit_error_validation():
    """Test token limit error validation"""
    with pytest.raises(ValueError):
        TokenLimitError(max_tokens=-1, actual_tokens=100)

    with pytest.raises(ValueError):
        TokenLimitError(max_tokens=100, actual_tokens=-1)


def test_error_equality():
    """Test error equality"""
    error1 = LLMError("Test error")
    error2 = LLMError("Test error")
    error3 = LLMError("Different error")

    assert error1 == error2
    assert error1 != error3
    assert hash(error1) == hash(error2)


def test_error_pickling():
    """Test error pickling"""
    import pickle

    original = LLMError("Test error", cause=ValueError("Original error"))
    pickled = pickle.dumps(original)
    unpickled = pickle.loads(pickled)

    assert unpickled.message == original.message
    assert str(unpickled.cause) == str(original.cause)


def test_error_with_unicode():
    """Test error with unicode message"""
    message = "Test error 测试错误 テストエラー"
    error = LLMError(message)
    assert str(error) == message
    assert error.message == message


def test_error_with_nested_cause():
    """Test error with nested cause"""
    inner = ValueError("Inner error")
    middle = RuntimeError("Middle error")
    middle.__cause__ = inner  # type: ignore
    error = LLMError("Outer error", cause=middle)

    assert error.message == "Outer error"
    assert error.cause == middle
    assert error.cause.__cause__ == inner  # type: ignore
