"""Base module implementations"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class InitializableModule(ABC):
    """Base class for modules that require initialization"""

    def __init__(self) -> None:
        self._initialized = False

    @property
    def is_initialized(self) -> bool:
        """Check if module is initialized"""
        return self._initialized

    async def initialize(self) -> None:
        """Initialize module"""
        if self._initialized:
            return

        await self._initialize()
        self._initialized = True

    async def cleanup(self) -> None:
        """Cleanup module resources"""
        if not self._initialized:
            return

        await self._cleanup()
        self._initialized = False

    @abstractmethod
    async def _initialize(self) -> None:
        """Implementation specific initialization"""
        pass

    @abstractmethod
    async def _cleanup(self) -> None:
        """Implementation specific cleanup"""
        pass

    def _ensure_initialized(self) -> None:
        """Ensure module is initialized"""
        if not self._initialized:
            raise RuntimeError(f"{self.__class__.__name__} not initialized")


class BaseModule(InitializableModule, Generic[T]):
    """Base module with configuration"""

    def __init__(self, config: T) -> None:
        super().__init__()
        self.config = config
