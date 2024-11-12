"""Data transformation implementation"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List

from ..exceptions import CoreError


class TransformError(CoreError):
    """Transform error"""

    pass


class TransformType(Enum):
    """Transform types"""

    CAST = "cast"
    FORMAT = "format"
    REPLACE = "replace"
    FILTER = "filter"
    MAP = "map"
    CUSTOM = "custom"


@dataclass
class Transform:
    """Data transform definition"""

    type: TransformType
    config: Dict[str, Any]


class Transformer:
    """Data transformer"""

    def __init__(self, transforms: List[Transform]):
        self.transforms = transforms

    def apply(self, data: Any) -> Any:
        """Apply transforms to data"""
        result = data

        for transform in self.transforms:
            try:
                if transform.type == TransformType.CAST:
                    result = self._cast(result, transform.config)
                elif transform.type == TransformType.FORMAT:
                    result = self._format(result, transform.config)
                elif transform.type == TransformType.REPLACE:
                    result = self._replace(result, transform.config)
                elif transform.type == TransformType.FILTER:
                    result = self._filter(result, transform.config)
                elif transform.type == TransformType.MAP:
                    result = self._map(result, transform.config)
                elif transform.type == TransformType.CUSTOM:
                    result = self._custom(result, transform.config)
            except Exception as e:
                raise TransformError(f"Transform {transform.type.value} failed: {str(e)}")

        return result

    def _cast(self, value: Any, config: Dict[str, Any]) -> Any:
        """Cast value to type"""
        target_type = config["type"]
        if target_type == "int":
            return int(value)
        elif target_type == "float":
            return float(value)
        elif target_type == "str":
            return str(value)
        elif target_type == "bool":
            return bool(value)
        elif target_type == "list":
            return list(value)
        elif target_type == "dict":
            return dict(value)
        raise TransformError(f"Unsupported cast type: {target_type}")

    def _format(self, value: str, config: Dict[str, Any]) -> str:
        """Format string value"""
        template = config["template"]
        try:
            return template.format(value)
        except KeyError as e:
            raise TransformError(f"Missing format key: {str(e)}")
        except ValueError as e:
            raise TransformError(f"Invalid format: {str(e)}")

    def _replace(self, value: str, config: Dict[str, Any]) -> str:
        """Replace in string value"""
        for old, new in config["replacements"].items():
            value = value.replace(old, new)
        return value

    def _filter(self, value: List[Any], config: Dict[str, Any]) -> List[Any]:
        """Filter list values"""
        if not isinstance(value, (list, tuple)):
            raise TransformError("Value must be a list")

        condition = config["condition"]
        return [x for x in value if condition(x)]

    def _map(self, value: List[Any], config: Dict[str, Any]) -> List[Any]:
        """Map list values"""
        if not isinstance(value, (list, tuple)):
            raise TransformError("Value must be a list")

        transform = config["transform"]
        return [transform(x) for x in value]

    def _custom(self, value: Any, config: Dict[str, Any]) -> Any:
        """Apply custom transform"""
        transform_func = config["function"]
        if not callable(transform_func):
            raise TransformError("Custom transform must be callable")
        return transform_func(value)
