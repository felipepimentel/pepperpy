"""Base module implementation"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel

from .base.types import JsonDict
from .exceptions.module import ModuleError

T = TypeVar("T", bound=BaseModel)


class BaseModule(ABC, Generic[T]):
    """Base module implementation"""

    def __init__(self, config: T) -> None:
        self.config = config
        self._initialized = False
        self._metadata: JsonDict = {}

    async def initialize(self) -> None:
        """Initialize module"""
        if not self._initialized:
            await self._initialize()
            self._initialized = True

    async def cleanup(self) -> None:
        """Cleanup module"""
        if self._initialized:
            await self._cleanup()
            self._initialized = False

    @property
    def is_initialized(self) -> bool:
        """Check if module is initialized"""
        return self._initialized

    @property
    def metadata(self) -> JsonDict:
        """Get module metadata"""
        return self._metadata

    def _ensure_initialized(self) -> None:
        """Ensure module is initialized"""
        if not self._initialized:
            raise ModuleError("Module not initialized")

    @abstractmethod
    async def _initialize(self) -> None:
        """Initialize module implementation"""
        ...

    @abstractmethod
    async def _cleanup(self) -> None:
        """Cleanup module implementation"""
        ...


__all__ = [
    "BaseModule",
]
