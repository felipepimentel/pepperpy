from typing import Dict, Any, Type
from .interfaces import ConfigInterface, LoggerInterface, DatabaseInterface, APIClientInterface

class Registry:
    """Registro central para componentes do Pepperpy."""
    
    _instances: Dict[str, Any] = {}
    _implementations: Dict[str, Type] = {}
    
    @classmethod
    def register_implementation(cls, interface_name: str, implementation: Type) -> None:
        """Registra uma implementação para uma interface."""
        cls._implementations[interface_name] = implementation
    
    @classmethod
    def get_implementation(cls, interface_name: str) -> Type:
        """Recupera uma implementação registrada."""
        if interface_name not in cls._implementations:
            raise KeyError(f"Nenhuma implementação registrada para {interface_name}")
        return cls._implementations[interface_name]
    
    @classmethod
    def get_instance(cls, interface_name: str, **kwargs) -> Any:
        """Recupera ou cria uma instância de uma implementação."""
        if interface_name not in cls._instances:
            implementation = cls.get_implementation(interface_name)
            cls._instances[interface_name] = implementation(**kwargs)
        return cls._instances[interface_name] 