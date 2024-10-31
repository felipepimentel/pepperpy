"""Multi-agent workflow implementation."""
from typing import List, Dict, Any
from dataclasses import dataclass

from ...llm.base import BaseLLM
from ...data.types import Document
from .base import Agent

@dataclass
class WorkflowStep:
    """Represents a step in a multi-agent workflow."""
    agent: str
    action: str
    input_mapping: Dict[str, str]
    output_mapping: Dict[str, str]

class Workflow:
    """Manages multi-agent workflows."""
    
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.steps: List[WorkflowStep] = []
        
    def add_step(self, step: WorkflowStep) -> None:
        """Add a step to the workflow."""
        self.steps.append(step)
        
    async def execute(
        self,
        agents: Dict[str, Agent],
        initial_input: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute the workflow."""
        current_data = initial_input.copy()
        results = []
        
        for step in self.steps:
            if step.agent not in agents:
                raise ValueError(f"Agent {step.agent} not found")
                
            # Map inputs
            step_input = {
                new_key: current_data[old_key]
                for new_key, old_key in step.input_mapping.items()
            }
            
            # Execute step
            agent = agents[step.agent]
            result = await agent.execute(step.action, **step_input)
            
            # Map outputs
            for new_key, old_key in step.output_mapping.items():
                current_data[new_key] = result[old_key]
                
            results.append(result)
            
        return {
            "results": results,
            "final_state": current_data
        } 