"""Agent type definitions"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class AgentState:
    """Agent state information"""
    is_busy: bool
    current_task: str
    last_active: str
    metrics: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate state"""
        if not self.current_task:
            raise ValueError("Current task cannot be empty")


@dataclass
class AgentStatus:
    """Agent status information"""
    online: bool
    health_check: str
    last_error: Optional[str] = None
    uptime: Optional[str] = None


@dataclass
class AgentCapability:
    """Agent capability definition"""
    name: str
    description: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    requires_context: bool = False

    def __post_init__(self) -> None:
        """Validate capability"""
        if not self.name:
            raise ValueError("Capability name cannot be empty")


@dataclass
class AgentMetrics:
    """Agent performance metrics"""
    tasks_completed: int
    success_rate: float
    average_response_time: float
    error_rate: float

    def __post_init__(self) -> None:
        """Validate metrics"""
        if self.tasks_completed < 0:
            raise ValueError("Tasks completed cannot be negative")
        if not 0 <= self.success_rate <= 1:
            raise ValueError("Success rate must be between 0 and 1")
        if not 0 <= self.error_rate <= 1:
            raise ValueError("Error rate must be between 0 and 1")
        if self.average_response_time < 0:
            raise ValueError("Average response time cannot be negative")
