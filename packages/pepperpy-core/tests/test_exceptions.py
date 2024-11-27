"""Test core exceptions"""

from pepperpy_core.exceptions import (
    CacheError,
    ConfigError,
    ModuleError,
    PepperPyError,
    ValidationError,
)


def test_base_error() -> None:
    """Test base error creation"""
    error = PepperPyError("test error")
    assert str(error) == "test error"
    assert error.cause is None
    assert error.metadata == {}


def test_error_with_cause() -> None:
    """Test error with cause"""
    cause = ValueError("original error")
    error = PepperPyError("test error", cause=cause)
    assert str(error) == "test error (caused by: original error)"
    assert error.cause == cause


def test_error_with_metadata() -> None:
    """Test error with metadata"""
    error = PepperPyError("test error", module="test", code=123)
    assert error.metadata == {"module": "test", "code": 123}


def test_module_error() -> None:
    """Test module error"""
    error = ModuleError("module error")
    assert isinstance(error, PepperPyError)
    assert str(error) == "module error"


def test_config_error() -> None:
    """Test config error"""
    error = ConfigError("config error")
    assert isinstance(error, PepperPyError)
    assert str(error) == "config error"


def test_cache_error() -> None:
    """Test cache error"""
    error = CacheError("cache error")
    assert isinstance(error, PepperPyError)
    assert str(error) == "cache error"


def test_validation_error() -> None:
    """Test validation error"""
    error = ValidationError("validation error")
    assert isinstance(error, PepperPyError)
    assert str(error) == "validation error"


def test_error_chaining() -> None:
    """Test error chaining"""
    try:
        try:
            raise ValueError("root cause")
        except ValueError as e:
            raise ConfigError("config failed", cause=e)
    except ConfigError as e:
        assert isinstance(e, PepperPyError)
        assert isinstance(e.cause, ValueError)
        assert str(e) == "config failed (caused by: root cause)"
