"""Keyboard input handling"""

import asyncio
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, Union

from .exceptions import InputError


class KeyCode(Enum):
    """Key codes"""

    ENTER = auto()
    ESCAPE = auto()
    BACKSPACE = auto()
    DELETE = auto()
    TAB = auto()
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    HOME = auto()
    END = auto()
    PAGE_UP = auto()
    PAGE_DOWN = auto()
    INSERT = auto()
    CTRL_C = auto()
    CTRL_D = auto()


@dataclass
class Key:
    """Keyboard key"""

    code: Union[KeyCode, str]
    alt: bool = False
    ctrl: bool = False
    shift: bool = False
    meta: bool = False
    modifiers: Dict[str, Any] = field(default_factory=dict)


class KeyboardManager:
    """Keyboard input manager"""

    def __init__(self):
        self._queue: asyncio.Queue[Key] = asyncio.Queue()
        self._running = False

    async def initialize(self) -> None:
        """Initialize keyboard manager"""
        self._running = True

    async def cleanup(self) -> None:
        """Cleanup keyboard manager"""
        self._running = False
        while not self._queue.empty():
            await self._queue.get()

    async def get_key(self) -> Key:
        """Get next key press

        Returns:
            Key: Next key press
        """
        try:
            return await self._queue.get()
        except Exception as e:
            raise InputError(f"Failed to get key: {str(e)}", cause=e)

    def put_key(self, key: Key) -> None:
        """Put key in queue

        Args:
            key: Key to put in queue
        """
        if self._running:
            self._queue.put_nowait(key)


# Common keys
ENTER = Key(KeyCode.ENTER)
ESCAPE = Key(KeyCode.ESCAPE)
BACKSPACE = Key(KeyCode.BACKSPACE)
DELETE = Key(KeyCode.DELETE)
TAB = Key(KeyCode.TAB)
UP = Key(KeyCode.UP)
DOWN = Key(KeyCode.DOWN)
LEFT = Key(KeyCode.LEFT)
RIGHT = Key(KeyCode.RIGHT)
HOME = Key(KeyCode.HOME)
END = Key(KeyCode.END)
PAGE_UP = Key(KeyCode.PAGE_UP)
PAGE_DOWN = Key(KeyCode.PAGE_DOWN)
INSERT = Key(KeyCode.INSERT)
CTRL_C = Key(KeyCode.CTRL_C)
CTRL_D = Key(KeyCode.CTRL_D)
