import re
from dataclasses import dataclass
from datetime import datetime
from typing import Callable, List, Optional


@dataclass
class ValidationRule:
    """Validation rule for input"""

    check: Callable[[str], bool]
    message: str


class InputValidator:
    """Input validation system"""

    @staticmethod
    def required(message: str = "This field is required") -> ValidationRule:
        """Field must not be empty"""
        return ValidationRule(lambda x: bool(x.strip()), message)

    @staticmethod
    def min_length(length: int, message: Optional[str] = None) -> ValidationRule:
        """Field must have minimum length"""
        return ValidationRule(
            lambda x: len(x) >= length,
            message or f"Must be at least {length} characters",
        )

    @staticmethod
    def max_length(length: int, message: Optional[str] = None) -> ValidationRule:
        """Field must have maximum length"""
        return ValidationRule(
            lambda x: len(x) <= length,
            message or f"Must be at most {length} characters",
        )

    @staticmethod
    def pattern(regex: str, message: str) -> ValidationRule:
        """Field must match regex pattern"""
        return ValidationRule(lambda x: bool(re.match(regex, x)), message)

    @staticmethod
    def email(message: str = "Invalid email address") -> ValidationRule:
        """Field must be valid email"""
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return InputValidator.pattern(email_regex, message)

    @staticmethod
    def date(format: str = "%Y-%m-%d", message: Optional[str] = None) -> ValidationRule:
        """Field must be valid date"""

        def check_date(value: str) -> bool:
            try:
                datetime.strptime(value, format)
                return True
            except ValueError:
                return False

        return ValidationRule(
            check_date, message or f"Must be valid date in format {format}"
        )

    @staticmethod
    def number(
        min_value: Optional[float] = None,
        max_value: Optional[float] = None,
        message: Optional[str] = None,
    ) -> ValidationRule:
        """Field must be valid number in range"""

        def check_number(value: str) -> bool:
            try:
                num = float(value)
                if min_value is not None and num < min_value:
                    return False
                if max_value is not None and num > max_value:
                    return False
                return True
            except ValueError:
                return False

        range_str = ""
        if min_value is not None:
            range_str += f">= {min_value}"
        if max_value is not None:
            range_str += " and " if range_str else ""
            range_str += f"<= {max_value}"

        return ValidationRule(
            check_number, message or f"Must be number {range_str if range_str else ''}"
        )

    def validate(self, value: str, rules: List[ValidationRule]) -> Optional[str]:
        """Validate value against rules"""
        for rule in rules:
            if not rule.check(value):
                return rule.message
        return None
