"""Common test fixtures and utilities"""

import sys
from pathlib import Path
from typing import Any, Dict

import pytest

# Add project root to Python path
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))


@pytest.fixture
def sample_config() -> Dict[str, Any]:
    """Provide sample configuration for testing"""
    return {"debug": True, "timeout": 30, "retries": 3}


@pytest.fixture
def temp_files(tmp_path: Path) -> Path:
    """Provide temporary directory for file operations"""
    return tmp_path
