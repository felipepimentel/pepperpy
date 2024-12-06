"""Validation type definitions."""

from dataclasses import dataclass, field
from typing import Any

from ..base import BaseConfigData


@dataclass
class ValidationResult(BaseConfigData):
    """Validation result data."""

    # Required fields (herdado de BaseConfigData)
    name: str

    # Optional fields
    valid: bool = True
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        """Validate result data."""
        if not isinstance(self.errors, list):
            raise ValueError("errors must be a list")
        if not isinstance(self.warnings, list):
            raise ValueError("warnings must be a list")

    def get_stats(self) -> dict[str, Any]:
        """Get validation result statistics."""
        return {
            "name": self.name,
            "valid": self.valid,
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
            "metadata": self.metadata,
        }


__all__ = ["ValidationResult"]
