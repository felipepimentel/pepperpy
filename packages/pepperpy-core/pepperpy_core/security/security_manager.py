"""Security manager implementation"""

from datetime import datetime, timedelta
from typing import Optional
from uuid import uuid4

from ..base.module import BaseModule
from .config import SecurityConfig
from .tokens import SecurityToken


class SecurityManager(BaseModule[SecurityConfig]):
    """Security manager implementation"""

    def __init__(self, config: Optional[SecurityConfig] = None) -> None:
        super().__init__(config or SecurityConfig.get_default())
        self._tokens: dict[str, SecurityToken] = {}

    async def _initialize(self) -> None:
        """Initialize security manager"""
        self._tokens.clear()

    async def _cleanup(self) -> None:
        """Cleanup security manager"""
        self._tokens.clear()

    async def create_token(self, user_id: str, expires_in: timedelta) -> SecurityToken:
        """Create security token"""
        self._ensure_initialized()

        token = SecurityToken(
            token=str(uuid4()), expires_at=datetime.utcnow() + expires_in, user_id=user_id
        )
        self._tokens[token.token] = token
        return token

    async def validate_token(self, token: str) -> bool:
        """Validate security token"""
        self._ensure_initialized()

        token_obj = self._tokens.get(token)
        if not token_obj:
            return False

        if token_obj.is_expired:
            self._tokens.pop(token)
            return False

        return True
