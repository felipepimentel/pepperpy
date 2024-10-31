"""Agent coordination and orchestration."""
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
import asyncio

from ...llm.base import BaseLLM
from ...llm.templates import PromptTemplate
from .base import Agent  # Importando Agent da base do módulo
from .types import AgentTask  # Movendo AgentTask para um arquivo de tipos

@dataclass
class AgentTask:
    """Represents a task for an agent."""
    name: str
    description: str
    required_skills: List[str]
    dependencies: List[str] = field(default_factory=list)
    priority: int = 1

class AgentCoordinator:
    """Coordinates multiple agents for complex tasks."""
    
    def __init__(self, llm: BaseLLM):
        self.llm = llm
        self.agents: Dict[str, Dict[str, Any]] = {}  # Tipagem mais específica
        self.tasks: Dict[str, AgentTask] = {}
        
    def register_agent(self, agent: 'Agent', skills: List[str]):  # String literal type hint
        """Register an agent with their skills."""
        self.agents[agent.name] = {
            "agent": agent,
            "skills": set(skills),
            "busy": False
        }
        
    async def execute_task(self, task: AgentTask, **kwargs) -> Dict[str, Any]:
        """Execute a task with the most suitable agent."""
        suitable_agents = self._find_suitable_agents(task)
        if not suitable_agents:
            raise ValueError(f"No suitable agent found for task: {task.name}")
            
        # Get least busy agent
        agent_info = min(
            suitable_agents,
            key=lambda x: self.agents[x["name"]]["busy"]
        )
        
        agent = self.agents[agent_info["name"]]["agent"]
        self.agents[agent_info["name"]]["busy"] = True
        
        try:
            return await agent.execute(task.name, **kwargs)
        finally:
            self.agents[agent_info["name"]]["busy"] = False
            
    async def execute_workflow(
        self,
        tasks: List[AgentTask],
        initial_input: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Execute a workflow of dependent tasks."""
        # Build dependency graph
        task_graph = self._build_task_graph(tasks)
        
        # Execute tasks respecting dependencies
        results = []
        current_input = initial_input.copy()
        
        while task_graph:
            # Find tasks with no dependencies
            available_tasks = [
                task for task, deps in task_graph.items()
                if not deps
            ]
            
            if not available_tasks:
                raise ValueError("Circular dependency detected")
                
            # Execute available tasks in parallel
            tasks_to_execute = [
                self.execute_task(task, **current_input)
                for task in available_tasks
            ]
            
            task_results = await asyncio.gather(*tasks_to_execute)
            results.extend(task_results)
            
            # Update task graph
            for task in available_tasks:
                del task_graph[task]
                for deps in task_graph.values():
                    deps.discard(task)
                    
            # Update input for next tasks
            for result in task_results:
                current_input.update(result.get("output", {}))
                
        return results 