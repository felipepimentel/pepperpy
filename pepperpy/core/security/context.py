"""Security context implementation"""

from pepperpy.core.module import BaseModule

from .config import SecurityConfig
from .types import AuthContext


class SecurityContext(BaseModule[SecurityConfig]):
    """Security context"""

    def __init__(self, config: SecurityConfig) -> None:
        super().__init__(config)
        self._auth_context: AuthContext | None = None

    async def _initialize(self) -> None:
        """Initialize security context"""
        self._auth_context = AuthContext()

    async def _cleanup(self) -> None:
        """Cleanup resources"""
        self._auth_context = None

    @property
    def auth_context(self) -> AuthContext | None:
        """Get current auth context"""
        return self._auth_context
