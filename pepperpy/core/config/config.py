"""Configuration management"""

import os
from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional

from dotenv import load_dotenv


@dataclass
class ConfigField:
    """Configuration field definition"""

    required: bool = False
    default: Any = None
    validator: Optional[Callable[[str], bool]] = None
    error: Optional[str] = None
    description: Optional[str] = None


class Config:
    """Configuration manager"""

    def __init__(self, fields: Dict[str, Dict[str, Any]]):
        load_dotenv()
        self._fields = {k: ConfigField(**v) for k, v in fields.items()}
        self._values: Dict[str, Any] = {}
        self._errors: Dict[str, str] = {}
        self._load_values()

    def _load_values(self) -> None:
        for key, field in self._fields.items():
            value = os.getenv(key, field.default)

            if value is None and field.required:
                self._errors[key] = f"Missing required environment variable: {key}"
                continue

            if value and field.validator and not field.validator(value):
                self._errors[key] = field.error or f"Invalid value for {key}"
                continue

            self._values[key] = value

    def is_valid(self) -> bool:
        return len(self._errors) == 0

    def get_errors(self) -> Dict[str, str]:
        return self._errors

    def as_dict(self) -> Dict[str, Any]:
        return self._values.copy()


def load_config(fields: Dict[str, Dict[str, Any]]) -> Config:
    """Load configuration from environment variables"""
    return Config(fields)
