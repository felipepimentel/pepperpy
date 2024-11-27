"""Test validators functionality"""

import pytest
from pepperpy_core.validation import ValidationLevel
from pepperpy_core.validation.validators import (
    LengthValidator,
    RegexValidator,
    TypeValidator,
)


@pytest.fixture
def regex_validator() -> RegexValidator:
    """Create regex validator"""
    return RegexValidator(r"^test_\d+$")


@pytest.fixture
def length_validator() -> LengthValidator:
    """Create length validator"""
    return LengthValidator(min_length=2, max_length=5)


@pytest.fixture
def type_validator() -> TypeValidator:
    """Create type validator"""
    return TypeValidator((str, int))


async def test_regex_validation(regex_validator: RegexValidator) -> None:
    """Test regex validation"""
    # Valid values
    result = await regex_validator.validate("test_123")
    assert result.valid
    assert result.level == ValidationLevel.INFO

    # Invalid values
    result = await regex_validator.validate("invalid")
    assert not result.valid
    assert result.level == ValidationLevel.ERROR
    assert "pattern" in result.metadata


async def test_regex_custom_message() -> None:
    """Test regex with custom message"""
    validator = RegexValidator(
        r"^\w+$", message="Invalid characters", level=ValidationLevel.WARNING
    )

    result = await validator.validate("@invalid@")
    assert not result.valid
    assert result.level == ValidationLevel.WARNING
    assert result.message == "Invalid characters"


async def test_length_validation(length_validator: LengthValidator) -> None:
    """Test length validation"""
    # Valid length
    result = await length_validator.validate("123")
    assert result.valid
    assert result.level == ValidationLevel.INFO
    assert result.metadata["length"] == 3

    # Too short
    result = await length_validator.validate("1")
    assert not result.valid
    assert "below minimum" in result.message

    # Too long
    result = await length_validator.validate("123456")
    assert not result.valid
    assert "above maximum" in result.message

    # Invalid type
    result = await length_validator.validate(123)
    assert not result.valid
    assert "does not support length" in result.message


async def test_type_validation(type_validator: TypeValidator) -> None:
    """Test type validation"""
    # Valid types
    result = await type_validator.validate("string")
    assert result.valid
    result = await type_validator.validate(123)
    assert result.valid

    # Invalid type
    result = await type_validator.validate(1.23)
    assert not result.valid
    assert "Expected type" in result.message
    assert "float" in result.metadata["actual_type"]


async def test_validate_many() -> None:
    """Test validating multiple values"""
    validator = RegexValidator(r"^\d+$")
    results = await validator.validate_many(["123", "abc", "456"])

    assert len(results) == 3
    assert results[0].valid  # "123"
    assert not results[1].valid  # "abc"
    assert results[2].valid  # "456"
