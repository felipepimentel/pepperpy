"""Security manager implementation"""

from typing import Optional

from pydantic import BaseModel

from ..module import BaseModule
from .types import SecurityContext, SecurityToken


class SecurityConfig(BaseModel):
    """Security configuration"""

    secret_key: str
    token_expiration: int = 3600  # 1 hour
    token_algorithm: str = "HS256"
    refresh_enabled: bool = True
    refresh_expiration: int = 86400  # 24 hours


class SecurityManager(BaseModule[SecurityConfig]):
    """Security manager implementation"""

    def __init__(self, config: SecurityConfig) -> None:
        super().__init__(config)
        self._context: Optional[SecurityContext] = None

    async def _initialize(self) -> None:
        """Initialize security manager"""
        self._context = SecurityContext(
            secret_key=self.config.secret_key, algorithm=self.config.token_algorithm
        )

    async def _cleanup(self) -> None:
        """Cleanup security manager"""
        self._context = None

    async def create_token(self, subject: str, **claims: str) -> SecurityToken:
        """Create security token"""
        self._ensure_initialized()
        if not self._context:
            raise RuntimeError("Security context not initialized")

        return await self._context.create_token(
            subject=subject, expiration=self.config.token_expiration, **claims
        )

    async def validate_token(self, token: str) -> bool:
        """Validate security token"""
        self._ensure_initialized()
        if not self._context:
            raise RuntimeError("Security context not initialized")

        return await self._context.validate_token(token)

    async def refresh_token(self, token: str) -> SecurityToken:
        """Refresh security token"""
        self._ensure_initialized()
        if not self.config.refresh_enabled:
            raise RuntimeError("Token refresh not enabled")
        if not self._context:
            raise RuntimeError("Security context not initialized")

        return await self._context.refresh_token(
            token=token, expiration=self.config.refresh_expiration
        )
