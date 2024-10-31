from typing import Any, Dict, Type
from .registry import Registry
from .interfaces import ConfigInterface, LoggerInterface, DatabaseInterface, APIClientInterface

class Factory:
    """Fábrica para criar instâncias de componentes."""
    
    @staticmethod
    def create_config(**kwargs) -> ConfigInterface:
        return Registry.get_instance('config', **kwargs)
    
    @staticmethod
    def create_logger(**kwargs) -> LoggerInterface:
        return Registry.get_instance('logger', **kwargs)
    
    @staticmethod
    def create_database(**kwargs) -> DatabaseInterface:
        return Registry.get_instance('database', **kwargs)
    
    @staticmethod
    def create_api_client(**kwargs) -> APIClientInterface:
        return Registry.get_instance('api_client', **kwargs) 