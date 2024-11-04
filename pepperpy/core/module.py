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
    """Classe base para módulos"""

    # Atributos de classe
    __module_name__: ClassVar[str]
    __version__: ClassVar[str] = "0.1.0"
    __description__: ClassVar[str] = ""
    __dependencies__: ClassVar[List[str]] = []

    def __init__(self, config: ModuleConfig):
        self.config = config
        self.logger = get_logger(self.__module_name__)

        # Componentes injetados
        self._event_bus: Optional[EventBus] = None
        self._context: Optional[Context] = None
        self._validator: Optional[Validator] = None

        # Estado
        self._initialized = False
        self._status = Status.INACTIVE

    @property
    def name(self) -> str:
        return self.__module_name__

    @property
    def status(self) -> Status:
        return self._status

    def _set_event_bus(self, event_bus: EventBus) -> None:
        self._event_bus = event_bus

    def _set_context(self, context: Context) -> None:
        self._context = context

    def _set_validator(self, validator: Validator) -> None:
        self._validator = validator

    async def initialize(self) -> None:
        """Inicializa o módulo"""
        try:
            # Validação
            if self._validator:
                errors = self._validator.validate(self.config.settings)
                if errors:
                    raise ValidationError(f"Invalid configuration: {errors}")

            # Hooks
            await self.pre_initialize()
            await self._initialize()
            await self.post_initialize()

            self._initialized = True
            self._status = Status.ACTIVE

            # Evento
            if self._event_bus:
                await self._event_bus.publish(
                    Event(
                        name="module.initialized",
                        source=self.name,
                        data={"status": self.status},
                    )
                )

        except Exception as e:
            self._status = Status.ERROR
            raise ModuleError(str(e), self.name) from e

    async def shutdown(self) -> None:
        """Finaliza o módulo"""
        try:
            await self.pre_shutdown()
            await self._shutdown()
            await self.post_shutdown()

            self._initialized = False
            self._status = Status.INACTIVE

            if self._event_bus:
                await self._event_bus.publish(
                    Event(name="module.shutdown", source=self.name)
                )

        except Exception as e:
            self._status = Status.ERROR
            raise ModuleError(str(e), self.name) from e

    # Hooks
    @abstractmethod
    async def pre_initialize(self) -> None:
        """Hook executado antes da inicialização"""
        pass

    @abstractmethod
    async def _initialize(self) -> None:
        """Implementação da inicialização"""
        pass

    @abstractmethod
    async def post_initialize(self) -> None:
        """Hook executado após a inicialização"""
        pass

    @abstractmethod
    async def pre_shutdown(self) -> None:
        """Hook executado antes do shutdown"""
        pass

    @abstractmethod
    async def _shutdown(self) -> None:
        """Implementação do shutdown"""
        pass

    @abstractmethod
    async def post_shutdown(self) -> None:
        """Hook executado após o shutdown"""
        pass

    # Utilitários
    def get_metadata(self) -> Metadata:
        """Obtém metadados do módulo"""
        return Metadata(
            name=self.name,
            version=self.__version__,
            description=self.__description__,
            tags=self.__dependencies__,
        )

    def get_service(self, name: str, service_type: Optional[Type[T]] = None) -> Any:
        """Obtém serviço do contexto"""
        if not self._context:
            raise ModuleError("Context not available", self.name)
        return self._context.get(name, service_type)

    async def emit(
        self, event_name: str, data: Optional[Dict[str, Any]] = None
    ) -> None:
        """Emite evento"""
        if not self._event_bus:
            raise ModuleError("Event bus not available", self.name)

        await self._event_bus.publish(
            Event(name=event_name, source=self.name, data=data)
        )

    @classmethod
    def create(cls: Type[T], **settings) -> T:
        """Factory method para criar módulo"""
        config = ModuleConfig(name=cls.__module_name__, settings=settings)
        return cls(config)
