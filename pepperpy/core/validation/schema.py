"""Schema validation implementation"""

import re
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from ..exceptions import CoreError


class ValidationError(CoreError):
    """Validation error"""

    def __init__(self, message: str, path: Optional[str] = None):
        super().__init__(message)
        self.path = path


class FieldType(Enum):
    """Field data types"""

    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    LIST = "list"
    DICT = "dict"
    ANY = "any"


@dataclass
class Field:
    """Schema field definition"""

    type: FieldType
    required: bool = True
    default: Any = None
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    min_value: Optional[Union[int, float]] = None
    max_value: Optional[Union[int, float]] = None
    pattern: Optional[str] = None
    choices: Optional[List[Any]] = None
    nested: Optional["Schema"] = None


class Schema:
    """Data validation schema"""

    def __init__(self, fields: Dict[str, Field]):
        self.fields = fields

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate data against schema"""
        result = {}
        errors = []

        for field_name, field in self.fields.items():
            try:
                value = data.get(field_name)

                # Check required
                if value is None:
                    if field.required:
                        raise ValidationError("Field is required")
                    result[field_name] = field.default
                    continue

                # Validate type
                value = self._validate_type(value, field)

                # Validate constraints
                self._validate_constraints(value, field)

                result[field_name] = value

            except ValidationError as e:
                e.path = field_name
                errors.append(e)

        if errors:
            raise ValidationError(
                "Validation failed", "\n".join(f"{e.path}: {str(e)}" for e in errors)
            )

        return result

    def _validate_type(self, value: Any, field: Field) -> Any:
        """Validate and convert value type"""
        try:
            if field.type == FieldType.STRING:
                return str(value)
            elif field.type == FieldType.INTEGER:
                return int(value)
            elif field.type == FieldType.FLOAT:
                return float(value)
            elif field.type == FieldType.BOOLEAN:
                if isinstance(value, str):
                    return value.lower() in ("true", "1", "yes", "on")
                return bool(value)
            elif field.type == FieldType.LIST:
                if not isinstance(value, (list, tuple)):
                    raise ValidationError("Must be a list")
                return list(value)
            elif field.type == FieldType.DICT:
                if not isinstance(value, dict):
                    raise ValidationError("Must be a dictionary")
                if field.nested:
                    return field.nested.validate(value)
                return dict(value)
            return value
        except (ValueError, TypeError):
            raise ValidationError(f"Invalid type, expected {field.type.value}")

    def _validate_constraints(self, value: Any, field: Field) -> None:
        """Validate field constraints"""
        if field.min_length is not None and len(value) < field.min_length:
            raise ValidationError(f"Length must be >= {field.min_length}")

        if field.max_length is not None and len(value) > field.max_length:
            raise ValidationError(f"Length must be <= {field.max_length}")

        if field.min_value is not None and value < field.min_value:
            raise ValidationError(f"Value must be >= {field.min_value}")

        if field.max_value is not None and value > field.max_value:
            raise ValidationError(f"Value must be <= {field.max_value}")

        if field.pattern and not re.match(field.pattern, str(value)):
            raise ValidationError(f"Value must match pattern: {field.pattern}")

        if field.choices and value not in field.choices:
            raise ValidationError(f"Value must be one of: {field.choices}")
