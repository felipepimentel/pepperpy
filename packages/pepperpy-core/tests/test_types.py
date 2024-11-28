"""Test core types"""

from typing import Dict

import pytest
from pepperpy_core.base.types import JsonDict, JsonValue


def test_json_dict_type() -> None:
    """Test JsonDict type"""
    data: JsonDict = {
        "str": "value",
        "int": 42,
        "float": 3.14,
        "bool": True,
        "null": None,
        "list": [1, 2, 3],
        "dict": {"key": "value"},
    }
    assert isinstance(data, Dict)


def test_json_value_type() -> None:
    """Test JsonValue type"""
    values: list[JsonValue] = ["string", 42, 3.14, True, None, [1, 2, 3], {"key": "value"}]
    for value in values:
        assert isinstance(value, (str, int, float, bool, list, dict)) or value is None


def test_json_dict_nested() -> None:
    """Test nested JsonDict"""
    data: JsonDict = {"level1": {"level2": {"level3": "value"}}}
    assert isinstance(data["level1"], dict)
    assert isinstance(data["level1"]["level2"], dict)
    assert isinstance(data["level1"]["level2"]["level3"], str)


def test_json_dict_invalid() -> None:
    """Test invalid JsonDict values"""

    def func() -> None:
        pass

    with pytest.raises((TypeError, ValueError)):
        data: JsonDict = {}
        data["func"] = func  # type: ignore
        # Força o erro tentando serializar
        import json

        json.dumps(data)