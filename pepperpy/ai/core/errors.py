"""AI-specific exceptions."""
from typing import Optional

class AIError(Exception):
    """Base exception for AI-related errors."""
    pass

class LLMError(AIError):
    """LLM-specific errors."""
    pass

class DataProcessingError(AIError):
    """Data processing errors."""
    pass

class PipelineError(AIError):
    """Pipeline execution errors."""
    pass

class ResourceExhaustedError(AIError):
    """Resource exhaustion errors (tokens, budget, etc)."""
    def __init__(
        self, 
        message: str, 
        resource_type: str,
        limit: float,
        current: float
    ):
        self.resource_type = resource_type
        self.limit = limit
        self.current = current
        super().__init__(
            f"{message} ({resource_type}: {current}/{limit})"
        ) 