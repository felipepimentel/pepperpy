"""Type definitions for agent module."""
from typing import List, Dict, Any, Protocol
from dataclasses import dataclass, field

@dataclass
class AgentTask:
    """Represents a task for an agent."""
    name: str
    description: str
    required_skills: List[str]
    dependencies: List[str] = field(default_factory=list)
    priority: int = 1

class AgentProtocol(Protocol):
    """Protocol defining agent interface."""
    name: str
    
    async def execute(self, task_name: str, **kwargs) -> Dict[str, Any]:
        """Execute a task."""
        ... 