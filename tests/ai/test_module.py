"""Tests for AI module"""

from unittest.mock import AsyncMock, create_autospec, patch

import pytest

from pepperpy.ai.exceptions import ProviderError
from pepperpy.ai.module import AIModule
from pepperpy.ai.providers.base import BaseProvider
from pepperpy.ai.types import AIResponse, Message
from pepperpy.core.base import ModuleStatus


@pytest.fixture
async def mock_provider():
    """Create a mock provider"""
    provider = create_autospec(BaseProvider, instance=True)
    provider.initialize = AsyncMock()
    provider.generate = AsyncMock()
    provider.cleanup = AsyncMock()
    provider.initialized = True
    return provider


@pytest.fixture
async def ai_module(sample_config, mock_provider):
    """Fixture for AI module with mocked provider"""
    with patch("pepperpy.ai.module.AIModule._get_provider_class") as mock_get_provider:
        mock_get_provider.return_value = lambda x: mock_provider
        module = AIModule(sample_config)
        await module.setup()
        module._status = ModuleStatus.ACTIVE  # Garantir status ativo após setup
        return module


@pytest.mark.asyncio
async def test_ai_module_initialization(ai_module, mock_provider):
    """Test AI module initialization"""
    assert ai_module._provider is not None
    assert mock_provider.initialize.call_count == 1


@pytest.mark.asyncio
async def test_ai_module_ask(ai_module, mock_provider):
    """Test simple ask method"""
    # Configure mock
    mock_response = AIResponse(
        content="Paris is the capital of France", model="test-model", provider="openrouter"
    )
    mock_provider.generate.return_value = mock_response

    # Test
    response = await ai_module.ask("What is the capital of France?")
    assert response == "Paris is the capital of France"

    # Verify mock was called correctly
    assert mock_provider.generate.call_count == 1
    call_args = mock_provider.generate.call_args[0][0]
    assert len(call_args) == 1
    assert isinstance(call_args[0], Message)
    assert call_args[0].role == "user"
    assert call_args[0].content == "What is the capital of France?"


@pytest.mark.asyncio
async def test_ai_module_generate_with_message(ai_module, mock_provider):
    """Test generate with Message object"""
    # Configure mock
    mock_response = AIResponse(content="Test response", model="test-model", provider="openrouter")
    mock_provider.generate.return_value = mock_response

    # Test with Message object
    message = Message(role="user", content="Test message")
    response = await ai_module.generate(message)

    assert response.content == "Test response"
    assert response.model == "test-model"
    assert response.provider == "openrouter"


@pytest.mark.asyncio
async def test_ai_module_cleanup(ai_module, mock_provider):
    """Test cleanup method"""
    await ai_module.cleanup()
    assert mock_provider.cleanup.call_count == 1


@pytest.mark.asyncio
async def test_ai_module_context_manager(sample_config, mock_provider):
    """Test context manager usage"""
    with patch("pepperpy.ai.module.AIModule._get_provider_class") as mock_get_provider:
        mock_get_provider.return_value = lambda x: mock_provider

        async with AIModule.session(sample_config) as ai:
            assert ai._provider is not None
            # Verificar se o módulo está ativo após inicialização
            assert ai._status == ModuleStatus.ACTIVE


@pytest.mark.asyncio
async def test_provider_error_handling(ai_module, mock_provider):
    """Test error handling"""
    # Configurar o mock para lançar uma exceção específica
    mock_provider.generate = AsyncMock(side_effect=RuntimeError("Test error"))

    # Verificar se a exceção é capturada e convertida em ProviderError
    with pytest.raises(ProviderError) as exc_info:
        await ai_module.ask("Test prompt")

    # Verificar a mensagem de erro
    assert "Test error" in str(exc_info.value)
    # Verificar se o mock foi chamado
    assert mock_provider.generate.call_count == 1
