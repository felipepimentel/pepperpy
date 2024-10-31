from dataclasses import dataclass, field
from typing import Dict, Optional, List

@dataclass
class TokenUsage:
    """Represents token usage in a call."""
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

@dataclass
class CostEstimate:
    """Represents the estimated cost of an operation."""
    prompt_cost: float
    completion_cost: float
    total_cost: float
    currency: str = "USD"

@dataclass
class Budget:
    """Represents a budget configuration."""
    max_cost: float
    max_tokens: Optional[int] = None
    currency: str = "USD"
    reset_on_exceed: bool = False
    
    def is_within_budget(self, current_cost: float, current_tokens: int) -> bool:
        """Check if the current usage is within budget."""
        if current_cost >= self.max_cost:
            return False
        if self.max_tokens and current_tokens >= self.max_tokens:
            return False
        return True

class TokenCounter:
    """Utility class for token counting."""
    
    @staticmethod
    def estimate_tokens(text: str) -> int:
        """
        Simple token estimation (4 characters = 1 token).
        Can be overridden with more precise implementations.
        """
        return len(text) // 4

    @classmethod
    def count_messages_tokens(cls, messages: List[Dict[str, str]]) -> int:
        """Count tokens in a list of messages."""
        return sum(cls.estimate_tokens(msg["content"]) for msg in messages)

class CostManager:
    """Cost manager for LLMs."""
    
    DEFAULT_COSTS = {
        "gpt-4": {"input": 0.03, "output": 0.06},
        "gpt-3.5-turbo": {"input": 0.001, "output": 0.002},
        "claude-3-opus": {"input": 0.015, "output": 0.075},
        "claude-3-sonnet": {"input": 0.003, "output": 0.015},
    }

    def __init__(self, budget: Optional[Budget] = None):
        self.budget = budget
        self._total_cost = 0.0
        self._total_tokens = 0

    @property
    def total_cost(self) -> float:
        return self._total_cost

    @property
    def total_tokens(self) -> int:
        return self._total_tokens

    def can_make_request(self, estimated_cost: float, estimated_tokens: int) -> bool:
        """Check if a request can be made within budget."""
        if not self.budget:
            return True
            
        future_cost = self._total_cost + estimated_cost
        future_tokens = self._total_tokens + estimated_tokens
        
        return self.budget.is_within_budget(future_cost, future_tokens)

    def track_usage(self, cost: float, tokens: int):
        """Track usage and handle budget limits."""
        self._total_cost += cost
        self._total_tokens += tokens
        
        if self.budget and not self.can_make_request(0, 0):
            if self.budget.reset_on_exceed:
                self.reset()
            raise BudgetExceededError(
                f"Budget exceeded: {self._total_cost:.2f} {self.budget.currency}"
            )

    def reset(self):
        """Reset usage counters."""
        self._total_cost = 0.0
        self._total_tokens = 0

    @classmethod
    def get_model_costs(cls, model: str) -> Dict[str, float]:
        """Get costs for a specific model."""
        clean_model = model.split('/')[-1]
        return cls.DEFAULT_COSTS.get(clean_model, {"input": 0.0, "output": 0.0})

    @classmethod
    def estimate_cost(
        cls,
        prompt_tokens: int,
        completion_tokens: int,
        model: str
    ) -> CostEstimate:
        """Calculate estimated cost based on token usage."""
        costs = cls.get_model_costs(model)
        
        prompt_cost = (prompt_tokens / 1000) * costs["input"]
        completion_cost = (completion_tokens / 1000) * costs["output"]
        
        return CostEstimate(
            prompt_cost=prompt_cost,
            completion_cost=completion_cost,
            total_cost=prompt_cost + completion_cost
        )

class BudgetExceededError(Exception):
    """Raised when budget limits are exceeded."""
    pass