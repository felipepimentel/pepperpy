"""Data validation and sanitization system."""
from typing import Any, Dict, Optional, Type, Union
from dataclasses import dataclass
import re
from pydantic import BaseModel, ValidationError

@dataclass
class SanitizeRule:
    """Rule for data sanitization."""
    pattern: str
    replacement: str
    description: str = ""

class DataValidator:
    """Validate and sanitize data."""
    
    DEFAULT_RULES = {
        "sql_injection": SanitizeRule(
            pattern=r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|UNION)\b)",
            replacement="",
            description="Remove SQL injection attempts"
        ),
        "xss": SanitizeRule(
            pattern=r"<[^>]*>",
            replacement="",
            description="Remove HTML/XML tags"
        ),
        "path_traversal": SanitizeRule(
            pattern=r"\.{2,}[/\\]",
            replacement="",
            description="Remove path traversal attempts"
        )
    }
    
    def __init__(self, custom_rules: Optional[Dict[str, SanitizeRule]] = None):
        """Initialize with optional custom rules."""
        self.rules = {**self.DEFAULT_RULES, **(custom_rules or {})}
    
    def sanitize(self, data: str, rules: Optional[list[str]] = None) -> str:
        """Sanitize string data using specified rules."""
        rules = rules or list(self.rules.keys())
        result = data
        
        for rule_name in rules:
            if rule := self.rules.get(rule_name):
                result = re.sub(rule.pattern, rule.replacement, result)
        
        return result
    
    def validate_model(self, data: Dict[str, Any], model: Type[BaseModel]) -> BaseModel:
        """Validate data against Pydantic model."""
        try:
            return model(**data)
        except ValidationError as e:
            raise ValueError(f"Validation failed: {e}") 