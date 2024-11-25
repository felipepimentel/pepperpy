"""Research agent implementation"""

from typing import Any, Dict, List, Optional

from pepperpy.ai.types import AIResponse
from pepperpy.core.exceptions import PepperPyError

from .base import BaseAgent


class ResearchAgent(BaseAgent):
    """Agent responsible for conducting research"""

    async def execute(self, task: str, **kwargs: Any) -> AIResponse:
        """Execute research task.
        
        Args:
            task: Task to execute
            **kwargs: Additional arguments for research
            
        Returns:
            AIResponse: Research results
            
        Raises:
            PepperPyError: If research fails
            RuntimeError: If agent is not initialized
        """
        return await self.research(task, **kwargs)

    async def research(
        self, 
        topic: str, 
        parameters: Optional[Dict[str, Any]] = None,
        sources: Optional[List[Dict[str, str]]] = None,
        include_citations: bool = False,
        include_summary: bool = False,
        **kwargs: Any
    ) -> AIResponse:
        """Research a topic with structured prompt.

        Args:
            topic: Topic to research
            parameters: Optional research parameters
            sources: Optional list of source documents
            include_citations: Whether to include citations
            include_summary: Whether to include summary
            **kwargs: Additional arguments for research

        Returns:
            AIResponse: Research results

        Raises:
            PepperPyError: If research fails
            RuntimeError: If agent is not initialized
        """
        self._ensure_initialized()
        
        prompt_parts = [
            f"Research topic: {topic}",
            "Provide comprehensive analysis including:",
            "- Current state",
            "- Key developments",
            "- Future implications"
        ]

        if parameters:
            prompt_parts.append(f"Parameters: {parameters}")

        if sources:
            prompt_parts.append(f"Sources: {sources}")

        if include_citations:
            prompt_parts.append("Include citations")

        if include_summary:
            prompt_parts.append("Include summary")

        prompt = "\n".join(prompt_parts)

        try:
            return await self._client.complete(prompt)
        except Exception as e:
            raise PepperPyError(f"Research failed: {e}", cause=e)

    async def cleanup(self) -> None:
        """Cleanup agent resources."""
        if self._client.is_initialized:
            await self._client.cleanup()
        self._initialized = False
