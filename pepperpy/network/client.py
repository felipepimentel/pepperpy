"""Network client implementation"""

from typing import Protocol

from pepperpy.core.module import BaseModule

from .config import NetworkConfig


class Session(Protocol):
    """Network session protocol"""

    async def close(self) -> None:
        """Close session"""
        ...


class NetworkClient(BaseModule[NetworkConfig]):
    """Network client implementation"""

    def __init__(self, config: NetworkConfig) -> None:
        super().__init__(config)
        self._session: Session | None = None

    async def _initialize(self) -> None:
        """Initialize network client"""
        # Initialize session
        pass

    async def _cleanup(self) -> None:
        """Cleanup resources"""
        if self._session:
            await self._session.close()
