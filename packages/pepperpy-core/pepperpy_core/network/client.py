"""Network client implementation"""

from typing import Any, Protocol

from bko.core.module import InitializableModule
from bko.core.validation import ValidatorFactory

from .config import NetworkConfig
from .exceptions import NetworkError


class Session(Protocol):
    """Network session protocol"""

    async def close(self) -> None:
        """Close session"""
        ...

    async def request(self, method: str, url: str, **kwargs: Any) -> Any:
        """Make HTTP request"""
        ...


class NetworkClient(InitializableModule):
    """Network client implementation"""

    def __init__(self, config: NetworkConfig) -> None:
        super().__init__()
        self.config = config
        self._config_validator = ValidatorFactory.create_schema_validator(NetworkConfig)
        self._session: Session | None = None

    async def _initialize(self) -> None:
        """Initialize network client"""
        result = await self._config_validator.validate(self.config.model_dump())
        if not result.is_valid:
            raise NetworkError(f"Invalid configuration: {', '.join(result.errors)}")

    async def _cleanup(self) -> None:
        """Cleanup resources"""
        if self._session:
            await self._session.close()
            self._session = None

    async def request(self, method: str, url: str, **kwargs: Any) -> Any:
        """Make HTTP request"""
        self._ensure_initialized()
        if not self._session:
            raise NetworkError("Session not initialized")

        try:
            return await self._session.request(method, url, **kwargs)
        except Exception as e:
            raise NetworkError(f"Request failed: {e}", cause=e)
