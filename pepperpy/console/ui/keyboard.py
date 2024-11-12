"""Keyboard input handling"""

import sys
import termios
import tty
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Key(Enum):
    """Common keyboard keys"""

    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    ENTER = "ENTER"
    ESC = "ESC"
    SPACE = "SPACE"
    BACKSPACE = "BACKSPACE"
    TAB = "TAB"
    CTRL_C = "CTRL_C"


@dataclass
class KeyEvent:
    """Keyboard event information"""

    key: Key
    char: Optional[str] = None
    ctrl: bool = False
    alt: bool = False


class KeyboardManager:
    """Manages keyboard input in raw mode"""

    def __init__(self):
        self._fd = sys.stdin.fileno()
        self._old_settings = None

    def __enter__(self):
        """Enter raw mode"""
        self._old_settings = termios.tcgetattr(self._fd)
        tty.setraw(self._fd)
        return self

    def __exit__(self, *args):
        """Restore terminal settings"""
        if self._old_settings:
            termios.tcsetattr(self._fd, termios.TCSADRAIN, self._old_settings)

    def get_key(self) -> KeyEvent:
        """Get next keyboard event"""
        char = sys.stdin.read(1)

        # Handle special keys
        if char == "\x1b":  # ESC sequence
            next_char = sys.stdin.read(1)
            if next_char == "[":
                code = sys.stdin.read(1)
                return KeyEvent(
                    key={"A": Key.UP, "B": Key.DOWN, "C": Key.RIGHT, "D": Key.LEFT}.get(
                        code, Key.ESC
                    )
                )
            return KeyEvent(key=Key.ESC)

        # Handle control keys
        elif ord(char) < 32:
            return KeyEvent(
                key={
                    "\r": Key.ENTER,
                    "\t": Key.TAB,
                    "\x7f": Key.BACKSPACE,
                    "\x03": Key.CTRL_C,
                    " ": Key.SPACE,
                }.get(char, char),
                ctrl=True,
            )

        # Regular character
        return KeyEvent(key=char, char=char)
