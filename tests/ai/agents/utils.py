"""Test utilities for agents"""

from typing import AsyncIterator, TypeVar

T = TypeVar("T")


class AsyncIteratorWrapper(AsyncIterator[T]):
    """Wrapper to make any iterable into an async iterator"""
    
    def __init__(self, items: list[T]):
        self.items = items
        self.index = 0
        
    def __aiter__(self):
        return self
        
    async def __anext__(self):
        if self.index >= len(self.items):
            raise StopAsyncIteration
        item = self.items[self.index]
        self.index += 1
        return item 