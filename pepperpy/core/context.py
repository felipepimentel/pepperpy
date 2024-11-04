from contextlib import contextmanager
from typing import Any, Dict, Optional, Type, TypeVar

from .exceptions import ContextError, ServiceNotFoundError

T = TypeVar("T")


class Context:
    """
    Contexto da aplicação com gerenciamento de estado e serviços
    """

    def __init__(self):
        self._services: Dict[str, Any] = {}
        self._state: Dict[str, Any] = {}

    def register(self, name: str, service: Any) -> None:
        """Registra um serviço no contexto"""
        if name in self._services:
            raise ContextError(f"Service '{name}' already registered")
        self._services[name] = service

    def get(self, name: str, expected_type: Optional[Type[T]] = None) -> T:
        """Obtém um serviço do contexto"""
        service = self._services.get(name)
        if service is None:
            raise ServiceNotFoundError(f"Service '{name}' not found")

        if expected_type and not isinstance(service, expected_type):
            raise ContextError(
                f"Service '{name}' is type {type(service)}, expected {expected_type}"
            )

        return service

    def has(self, name: str) -> bool:
        """Verifica se um serviço existe"""
        return name in self._services

    # Gerenciamento de estado
    def set_state(self, key: str, value: Any) -> None:
        """Define um valor no estado"""
        self._state[key] = value

    def get_state(self, key: str, default: Any = None) -> Any:
        """Obtém um valor do estado"""
        return self._state.get(key, default)

    def clear_state(self, key: str) -> None:
        """Remove um valor do estado"""
        self._state.pop(key, None)

    @contextmanager
    def state_scope(self, **kwargs):
        """Contexto temporário para estado"""
        previous = {}
        try:
            # Salva estado anterior
            for key, value in kwargs.items():
                previous[key] = self._state.get(key)
                self._state[key] = value
            yield
        finally:
            # Restaura estado anterior
            for key, value in previous.items():
                if value is None:
                    self._state.pop(key, None)
                else:
                    self._state[key] = value

    # Utilitários
    def inject(self, cls: Type[T]) -> T:
        """Injeção de dependência automática baseada em type hints"""
        if not hasattr(cls, "__annotations__"):
            return cls()

        deps = {}
        for name, type_hint in cls.__annotations__.items():
            if name in self._services:
                deps[name] = self.get(name, type_hint)

        return cls(**deps)

    def snapshot(self) -> Dict[str, Any]:
        """Cria snapshot do estado atual"""
        return {"services": list(self._services.keys()), "state": dict(self._state)}
