"""Test security functionality"""

from datetime import timedelta

import pytest
from pepperpy_core.security import SecurityToken
from pepperpy_core.utils.datetime import utc_now


@pytest.mark.asyncio
async def test_security_token_expiration() -> None:
    """Test security token expiration"""
    # Create token that expires in 1 hour
    expires_at = utc_now() + timedelta(hours=1)
    token = SecurityToken(token="test_token", expires_at=expires_at, user_id="test_user")

    # Should not be expired
    assert not token.is_expired

    # Create expired token
    expired_at = utc_now() - timedelta(hours=1)
    expired_token = SecurityToken(token="expired_token", expires_at=expired_at, user_id="test_user")

    # Should be expired
    assert expired_token.is_expired


@pytest.mark.asyncio
async def test_security_token_metadata() -> None:
    """Test security token metadata"""
    token = SecurityToken(
        token="test_token",
        expires_at=utc_now() + timedelta(hours=1),
        user_id="test_user",
        metadata={"role": "admin"},
    )

    assert token.metadata["role"] == "admin"
