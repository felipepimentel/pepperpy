from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Callable
from .base import BaseLLM, LLMResponse
from .templates import PromptTemplate

@dataclass
class Agent:
    """Represents an AI agent with specific capabilities."""
    name: str
    description: str
    llm: BaseLLM
    system_prompt: str
    templates: Dict[str, PromptTemplate] = field(default_factory=dict)
    memory: List[Dict[str, str]] = field(default_factory=list)
    
    def __post_init__(self):
        """Initialize agent's memory with system prompt."""
        if self.system_prompt:
            self.memory.append({"role": "system", "content": self.system_prompt})
    
    def execute(self, template_name: str, **kwargs) -> LLMResponse:
        """Execute a specific template."""
        if template_name not in self.templates:
            raise ValueError(f"Template not found: {template_name}")
            
        template = self.templates[template_name]
        prompt = template.format(**kwargs)
        
        self.memory.append({"role": "user", "content": prompt})
        response = self.llm.chat(self.memory.copy())
        self.memory.append({"role": "assistant", "content": response.content})
        
        return response

class MultiAgentSystem:
    """Orchestrates multiple agents working together."""
    
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.workflows: Dict[str, List[Dict[str, Any]]] = {}
    
    def register_agent(self, agent: Agent):
        """Register an agent in the system."""
        self.agents[agent.name] = agent
    
    def register_workflow(self, name: str, steps: List[Dict[str, Any]]):
        """Register a multi-agent workflow."""
        self.workflows[name] = steps
    
    def execute_workflow(self, workflow_name: str, initial_input: Dict[str, Any]) -> List[Any]:
        """Execute a registered workflow."""
        if workflow_name not in self.workflows:
            raise ValueError(f"Workflow not found: {workflow_name}")
            
        results = []
        current_input = initial_input
        
        for step in self.workflows[workflow_name]:
            agent_name = step["agent"]
            template_name = step["template"]
            
            if agent_name not in self.agents:
                raise ValueError(f"Agent not found: {agent_name}")
                
            agent = self.agents[agent_name]
            response = agent.execute(template_name, **current_input)
            results.append(response)
            
            # Update input for next step if needed
            if "output_processor" in step:
                current_input = step["output_processor"](response, current_input)
            
        return results 