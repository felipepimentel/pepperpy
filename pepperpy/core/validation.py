from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, TypeVar

T = TypeVar("T")


@dataclass
class ValidationError:
    """Validation error details"""

    field: str
    message: str
    code: str


class Validator(ABC):
    """Base validator interface"""

    @abstractmethod
    def validate(self, value: Any) -> List[ValidationError]:
        """Validate a value"""
        pass


class ModuleValidator(Validator):
    """Module configuration validator"""

    def __init__(self, rules: Dict[str, Validator]) -> None:
        self.rules = rules

    def validate(self, config: Dict[str, Any]) -> List[ValidationError]:
        """Validate module configuration"""
        errors = []
        for field, validator in self.rules.items():
            if field in config:
                field_errors = validator.validate(config[field])
                errors.extend(field_errors)
        return errors
