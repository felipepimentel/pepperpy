"""Tool support for LLMs."""
from typing import Callable, Dict, Any, List, Optional
from dataclasses import dataclass, field
from pydantic import BaseModel, create_model

@dataclass
class Tool:
    """Represents a tool that can be used by the LLM."""
    name: str
    description: str
    function: Callable
    parameters: Dict[str, Any]
    required_params: List[str] = field(default_factory=list)

    def __post_init__(self):
        """Create a Pydantic model for parameters validation."""
        self.model = create_model(
            f"{self.name}Parameters",
            **{
                k: (v, ... if k in self.required_params else None)
                for k, v in self.parameters.items()
            }
        )

    def validate_and_execute(self, **kwargs) -> Any:
        """Validate parameters and execute the tool."""
        params = self.model(**kwargs)
        return self.function(**params.dict())

class ToolManager:
    """Manages available tools for LLM."""

    def __init__(self):
        self.tools: Dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        """Register a new tool."""
        self.tools[tool.name] = tool

    def get_tool(self, name: str) -> Optional[Tool]:
        """Get a registered tool by name."""
        return self.tools.get(name)

    def list_tools(self) -> List[Dict[str, Any]]:
        """List all available tools in function-calling format."""
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "parameters": {
                    "type": "object",
                    "properties": tool.parameters,
                    "required": tool.required_params
                }
            }
            for tool in self.tools.values()
        ] 