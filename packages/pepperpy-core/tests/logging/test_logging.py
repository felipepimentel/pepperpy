"""Logging tests."""

from collections.abc import AsyncGenerator
from typing import Any
from unittest.mock import AsyncMock

import pytest
from pepperpy_core.base import BaseModule
from pepperpy_core.logging.log_config import LogConfig


class MockLogManager(BaseModule[LogConfig]):
    """Mock log manager for testing."""

    def __init__(self, config: LogConfig) -> None:
        """Initialize mock log manager."""
        super().__init__(config)
        self.logs: list[str] = []
        self.metadata: list[dict[str, Any]] = []
        self.debug = AsyncMock()
        self.info = AsyncMock()
        self.warning = AsyncMock()
        self.error = AsyncMock()

        # Setup mock side effects
        self.debug.side_effect = self._log_debug
        self.info.side_effect = self._log_info
        self.warning.side_effect = self._log_warning
        self.error.side_effect = self._log_error

    async def _setup(self) -> None:
        """Setup mock."""
        pass

    async def _teardown(self) -> None:
        """Teardown mock."""
        pass

    async def get_stats(self) -> dict[str, Any]:
        """Get mock stats."""
        return {
            "name": self.config.name,
            "logs": len(self.logs),
            "metadata": len(self.metadata),
        }

    def _log_debug(self, message: str, **kwargs: Any) -> None:
        """Log debug message."""
        self.logs.append(f"DEBUG: {message}")
        self.metadata.append(kwargs)

    def _log_info(self, message: str, **kwargs: Any) -> None:
        """Log info message."""
        self.logs.append(f"INFO: {message}")
        self.metadata.append(kwargs)

    def _log_warning(self, message: str, **kwargs: Any) -> None:
        """Log warning message."""
        self.logs.append(f"WARNING: {message}")
        self.metadata.append(kwargs)

    def _log_error(self, message: str, **kwargs: Any) -> None:
        """Log error message."""
        self.logs.append(f"ERROR: {message}")
        self.metadata.append(kwargs)


@pytest.fixture
def log_config() -> LogConfig:
    """Create test log config."""
    return LogConfig(name="test")


@pytest.fixture
async def log_manager(log_config: LogConfig) -> AsyncGenerator[MockLogManager, None]:
    """Create test log manager."""
    manager = MockLogManager(config=log_config)
    await manager.initialize()
    try:
        yield manager
    finally:
        await manager.cleanup()


@pytest.mark.asyncio
async def test_log_manager_levels(log_manager: MockLogManager) -> None:
    """Test log manager levels."""
    await log_manager.debug("Debug message")
    await log_manager.info("Info message")
    await log_manager.warning("Warning message")
    await log_manager.error("Error message")

    assert "DEBUG: Debug message" in log_manager.logs
    assert "INFO: Info message" in log_manager.logs
    assert "WARNING: Warning message" in log_manager.logs
    assert "ERROR: Error message" in log_manager.logs


@pytest.mark.asyncio
async def test_log_manager_metadata(log_manager: MockLogManager) -> None:
    """Test log manager metadata."""
    await log_manager.info("Test message", user="test_user", action="test_action")
    assert {"user": "test_user", "action": "test_action"} in log_manager.metadata
