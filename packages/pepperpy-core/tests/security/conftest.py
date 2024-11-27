"""Security test configuration"""

import pytest
from pepperpy_core.security import SecurityConfig, SecurityManager


@pytest.fixture
def security_config() -> SecurityConfig:
    """Create security configuration"""
    return SecurityConfig.get_default()


@pytest.fixture
async def security_manager(security_config: SecurityConfig) -> SecurityManager:
    """Create security manager"""
    manager = SecurityManager(security_config)
    await manager.initialize()
    yield manager
    await manager.cleanup()
