"""Test logging functionality"""

from typing import Any

import pytest

from pepperpy_core.logging.config import LogConfig
from pepperpy_core.logging.manager import LogManager
from pepperpy_core.logging.types import LogLevel


class MockLogManager(LogManager):
    """Mock log manager for testing"""

    def __init__(self, config: LogConfig) -> None:
        super().__init__(config)
        self.logs: list[str] = []
        self._log_metadata: list[dict[str, Any]] = []

    def debug(self, message: str, **kwargs: Any) -> None:
        """Log debug message"""
        self.logs.append(f"DEBUG: {message}")
        self._log_metadata.append(kwargs)

    def info(self, message: str, **kwargs: Any) -> None:
        """Log info message"""
        self.logs.append(f"INFO: {message}")
        self._log_metadata.append(kwargs)

    def warning(self, message: str, **kwargs: Any) -> None:
        """Log warning message"""
        self.logs.append(f"WARNING: {message}")
        self._log_metadata.append(kwargs)

    def error(self, message: str, **kwargs: Any) -> None:
        """Log error message"""
        self.logs.append(f"ERROR: {message}")
        self._log_metadata.append(kwargs)


@pytest.fixture
async def log_manager() -> MockLogManager:
    """Create mock log manager"""
    config = LogConfig(name="test", level=str(LogLevel.DEBUG.value))
    manager = MockLogManager(config)
    await manager.initialize()
    return manager


async def test_log_manager_levels(log_manager: MockLogManager) -> None:
    """Test log manager levels"""
    log_manager.debug("Debug message")
    log_manager.info("Info message")
    log_manager.warning("Warning message")
    log_manager.error("Error message")

    assert "DEBUG: Debug message" in log_manager.logs
    assert "INFO: Info message" in log_manager.logs
    assert "WARNING: Warning message" in log_manager.logs
    assert "ERROR: Error message" in log_manager.logs


async def test_log_manager_metadata(log_manager: MockLogManager) -> None:
    """Test log manager metadata"""
    log_manager.info("Test message", user="test_user", action="test_action")

    assert {"user": "test_user", "action": "test_action"} in log_manager._log_metadata
