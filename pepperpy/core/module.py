"""Base module implementation"""

from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Generic, TypeVar

from .types import JsonDict

ConfigT = TypeVar("ConfigT")


class ModuleStatus(Enum):
    """Module status"""

    UNINITIALIZED = auto()
    INITIALIZING = auto()
    INITIALIZED = auto()
    ERROR = auto()
    TERMINATED = auto()


class BaseModule(ABC, Generic[ConfigT]):
    """Base module class"""

    def __init__(self, config: ConfigT) -> None:
        """Initialize module.

        Args:
            config: Module configuration
        """
        self._status = ModuleStatus.UNINITIALIZED
        self._initialized = False
        self._config = config
        self._metadata: JsonDict = {}

    @property
    def status(self) -> ModuleStatus:
        """Get module status"""
        return self._status

    @property
    def config(self) -> ConfigT:
        """Get module configuration"""
        if self._config is None:
            raise ValueError("Module configuration not set")
        return self._config

    @property
    def metadata(self) -> JsonDict:
        """Get module metadata"""
        return self._metadata

    async def initialize(self) -> None:
        """Initialize module"""
        if self._initialized:
            return

        try:
            self._status = ModuleStatus.INITIALIZING
            await self._initialize()
            self._status = ModuleStatus.INITIALIZED
            self._initialized = True
        except Exception as e:
            self._status = ModuleStatus.ERROR
            raise e

    @abstractmethod
    async def _initialize(self) -> None:
        """Initialize module implementation"""
        pass

    async def cleanup(self) -> None:
        """Cleanup module resources"""
        if not self._initialized:
            return

        try:
            await self._cleanup()
            self._status = ModuleStatus.TERMINATED
            self._initialized = False
        except Exception as e:
            self._status = ModuleStatus.ERROR
            raise e

    @abstractmethod
    async def _cleanup(self) -> None:
        """Cleanup module implementation"""
        pass

    @property
    def is_initialized(self) -> bool:
        """Check if module is initialized"""
        return self._initialized
