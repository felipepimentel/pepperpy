"""Common test fixtures and utilities"""

import sys
from pathlib import Path
from typing import Any, Dict

import pytest
from dotenv import load_dotenv

# Adicionar o diretório raiz ao PYTHONPATH
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

# Carregar variáveis de ambiente para testes
load_dotenv()


@pytest.fixture
def sample_config() -> Dict[str, Any]:
    """Provide sample configuration for testing"""
    return {
        "provider": "openrouter",
        "api_key": "test_key",
        "model": "test-model",
        "debug": True,
        "timeout": 30.0,
        "max_retries": 3,
    }


@pytest.fixture
def mock_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Setup mock environment variables"""
    monkeypatch.setenv("AI_PROVIDER", "openrouter")
    monkeypatch.setenv("OPENROUTER_API_KEY", "test_key")
    monkeypatch.setenv("OPENROUTER_MODEL", "test-model")


@pytest.fixture
def temp_files(tmp_path: Path) -> Path:
    """Provide temporary directory for file operations"""
    return tmp_path


@pytest.fixture(autouse=True)
def setup_test_env(mock_env: None) -> None:
    """Setup test environment"""
    # Configurar ambiente de teste aqui se necessário
    pass
