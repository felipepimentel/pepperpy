"""Agent team management implementation"""

from ....console import Console
from ...types import AIResponse, Message
from ..config import TeamConfig
from ..types import ReviewResult, TaskPlan, TaskResult
from .base import AutoGenAgent


class AgentTeam:
    """Manages a team of collaborative agents"""

    def __init__(self, agents: list[AutoGenAgent], config: TeamConfig | None = None):
        self.agents = {agent.name: agent for agent in agents}
        self.config = config or TeamConfig()
        self.console = Console()
        self._validate_team()

    def _validate_team(self) -> None:
        """Validate team composition and roles"""
        required_roles = {"planner", "executor", "critic"}
        team_roles = {agent.role for agent in self.agents.values()}

        if not required_roles.issubset(team_roles):
            missing = required_roles - team_roles
            raise ValueError(f"Missing required roles: {missing}")

    async def execute_task(self, task: str) -> TaskResult:
        """Execute task using the agent team"""
        try:
            # 1. Plan task
            plan = await self._get_plan(task)
            self.console.info(f"📋 Created plan with {len(plan.steps)} steps")

            # 2. Execute steps
            results = []
            for step in plan.steps:
                self.console.info(f"🔄 Executing step: {step[:100]}...")
                result = await self._execute_step(step)
                results.append(result)

                # 3. Review result
                review = await self._review_result(result)
                if not review.approved:
                    self.console.warning(f"⚠️ Review failed: {review.feedback}")
                    # Handle revision
                    revised_result = await self._revise_task(step, review.feedback)
                    results[-1] = revised_result
                else:
                    self.console.success("✅ Review passed")

            # 4. Compile final result
            return self._compile_results(task, results)

        except Exception as e:
            self.console.error(f"❌ Task execution failed: {e!s}")
            raise

    async def _get_plan(self, task: str) -> TaskPlan:
        """Get task execution plan from planner"""
        planner = self._get_agent_by_role("planner")
        response = await planner.send(f"Plan execution for task: {task}")
        return self._parse_plan(response)

    async def _execute_step(self, step: str) -> AIResponse:
        """Execute single step using appropriate agent"""
        executor = self._get_agent_by_role("executor")
        return await executor.send(step)

    async def _review_result(self, result: AIResponse) -> ReviewResult:
        """Review step result"""
        critic = self._get_agent_by_role("critic")
        response = await critic.send(f"Review result: {result.content}")
        return self._parse_review(response)

    async def _revise_task(self, task: str, feedback: str) -> AIResponse:
        """Revise task based on feedback"""
        executor = self._get_agent_by_role("executor")
        prompt = f"""Revise the following task based on feedback:

Task: {task}

Feedback: {feedback}

Please address all feedback points and provide an improved solution.
"""
        return await executor.send(prompt)

    def _parse_plan(self, response: AIResponse) -> TaskPlan:
        """Parse planning response into structured plan"""
        # Implementar lógica de parsing do plano
        steps = [
            step.strip()
            for step in response.content.split("\n")
            if step.strip() and not step.startswith("#")
        ]
        return TaskPlan(steps=steps)

    def _parse_review(self, response: AIResponse) -> ReviewResult:
        """Parse review response into structured result"""
        content = response.content.lower()

        # Análise simplificada do feedback
        approved = "approved" in content or "passed" in content
        changes = [
            line.strip()
            for line in response.content.split("\n")
            if line.strip() and line.startswith("-")
        ]

        return ReviewResult(approved=approved, feedback=response.content, changes_required=changes)

    def _compile_results(self, task: str, results: list[AIResponse]) -> TaskResult:
        """Compile individual results into final result"""
        # Combinar resultados em um resultado final
        combined_content = "\n\n".join(r.content for r in results)

        return TaskResult(
            success=True,
            output=combined_content,
            steps=[{"content": r.content, "metadata": r.metadata} for r in results],
        )

    def _get_agent_by_role(self, role: str) -> AutoGenAgent:
        """Get agent by role"""
        for agent in self.agents.values():
            if agent.role == role:
                return agent
        raise ValueError(f"No agent found for role: {role}")

    def broadcast(self, message: str) -> None:
        """Broadcast message to all agents"""
        for agent in self.agents.values():
            self.console.info(f"📢 Broadcasting to {agent.name}: {message}")
            agent.add_to_context(Message(content=message, sender="system"))

    def get_agent(self, name: str) -> AutoGenAgent | None:
        """Get agent by name"""
        return self.agents.get(name)

    def add_agent(self, agent: AutoGenAgent) -> None:
        """Add new agent to team"""
        self.agents[agent.name] = agent
        self._validate_team()

    def remove_agent(self, name: str) -> None:
        """Remove agent from team"""
        if name in self.agents:
            del self.agents[name]
            self._validate_team()
