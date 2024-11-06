from abc import ABC, abstractmethod
from typing import Any, ClassVar, Dict, List, Optional, Type, TypeVar

from .context import Context
from .events import Event, EventBus
from .exceptions import ModuleError, ValidationError
from .logging import get_logger
from .types import Metadata, ModuleConfig, Status
from .validation import Validator

T = TypeVar("T", bound="Module")


class Module(ABC):
    """Base class for all PepperPy modules with enhanced lifecycle management"""

    # Atributos de classe
    __module_name__: ClassVar[str]
    __version__: ClassVar[str]
    __description__: ClassVar[str]
    __dependencies__: ClassVar[List[str]]

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self._config = self._validate_config(config or {})
        self._status = Status.INACTIVE
        self._metadata = ModuleMetadata(
            name=self.__module_name__,
            version=self.__version__,
            description=self.__description__,
            dependencies=self.__dependencies__
        )
        self._logger = get_logger(self.__module_name__)
        self._event_bus = EventBus()
        self._context = Context()

    @abstractmethod
    async def setup(self) -> None:
        """Initialize module resources"""
        pass

    @abstractmethod
    async def cleanup(self) -> None:
        """Cleanup module resources"""
        pass

    async def health_check(self) -> HealthStatus:
        """Perform module health check"""
        return HealthStatus(
            module=self.__module_name__,
            status=self._status,
            details=self._get_health_details()
        )

    def _get_health_details(self) -> Dict[str, Any]:
        """Get detailed health information"""
        return {
            "version": self.__version__,
            "status": self._status,
            "config": self._config
        }
