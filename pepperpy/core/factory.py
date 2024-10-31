from typing import Any, Dict, Type
from .registry import Registry
from .interfaces import (
    ConfigInterface, 
    LoggerInterface, 
    DatabaseInterface, 
    APIClientInterface,
    ValidatorInterface,
    RateLimiterInterface,
    PluginInterface,
    EventDispatcherInterface,
    TelemetryInterface
)

class Factory:
    """Factory for creating component instances."""
    
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
    
    @staticmethod
    def create_validator(**kwargs) -> ValidatorInterface:
        return Registry.get_instance('validator', **kwargs)
    
    @staticmethod
    def create_rate_limiter(**kwargs) -> RateLimiterInterface:
        return Registry.get_instance('rate_limiter', **kwargs)
    
    @staticmethod
    def create_plugin_manager(**kwargs) -> PluginInterface:
        return Registry.get_instance('plugin_manager', **kwargs)
    
    @staticmethod
    def create_event_dispatcher(**kwargs) -> EventDispatcherInterface:
        return Registry.get_instance('event_dispatcher', **kwargs)
    
    @staticmethod
    def create_telemetry(**kwargs) -> TelemetryInterface:
        return Registry.get_instance('telemetry', **kwargs) 