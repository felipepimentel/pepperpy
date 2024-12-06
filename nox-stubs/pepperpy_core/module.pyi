"""Type stubs for pepperpy_core.module"""
from abc import ABC
from typing import Generic, TypeVar

T = TypeVar('T')

class BaseModule(Generic[T], ABC):
    """Base module type stub."""
    
    def __init__(self, config: T) -> None: ...
    
    async def initialize(self) -> None: ...
    
    async def cleanup(self) -> None: ...
    
    async def _setup(self) -> None: ...
    
    async def _teardown(self) -> None: ... 