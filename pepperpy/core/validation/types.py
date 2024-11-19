"""Validation type definitions"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ValidationResult:
    """Validation result"""
    valid: bool
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict) 