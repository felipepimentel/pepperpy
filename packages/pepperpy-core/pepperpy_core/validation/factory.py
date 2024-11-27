"""Validator factory implementations"""

from typing import Any, Type

from pydantic import BaseModel

from .base import Validator
from .validators import PydanticValidator, TypeValidator


class ValidatorFactory:
    """Factory for creating validators"""

    @staticmethod
    def create_schema_validator(model: Type[BaseModel]) -> Validator[BaseModel, dict[str, Any]]:
        """Create schema validator"""
        return PydanticValidator(model)

    @staticmethod
    def create_type_validator(type_: Type[Any]) -> Validator[Any, Any]:
        """Create type validator"""
        return TypeValidator(type_)
