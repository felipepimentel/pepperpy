"""Analysis agent implementation"""

from typing import Any, Dict, Optional

from bko.ai.types import AIResponse
from bko.core.exceptions import PepperPyError

from .base import BaseAgent


class AnalysisAgent(BaseAgent):
    """Analysis agent implementation"""

    async def execute(self, task: str, **kwargs: Any) -> AIResponse:
        """Execute analysis task.

        Args:
            task: Task to execute
            **kwargs: Additional arguments for analysis

        Returns:
            AIResponse: Analysis results

        Raises:
            PepperPyError: If analysis fails
            RuntimeError: If agent is not initialized
        """
        return await self.analyze(task, **kwargs)

    async def analyze(
        self,
        data: str,
        depth: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> AIResponse:
        """Analyze data with structured prompt.

        Args:
            data: Data to analyze
            depth: Optional analysis depth
            context: Optional analysis context
            **kwargs: Additional arguments for analysis

        Returns:
            AIResponse: Analysis results

        Raises:
            PepperPyError: If analysis fails
            RuntimeError: If agent is not initialized
        """
        self._ensure_initialized()
        prompt = (
            f"As an analyst with the role of {self.config.role}, "
            f"please analyze:\n\n{data}\n\n"
            "Include:\n"
            "- Key findings\n"
            "- Patterns\n"
            "- Insights\n"
            "- Recommendations"
        )

        if depth:
            prompt += f"\n\nAnalysis depth: {depth}"

        if context:
            prompt += f"\n\nContext:\n{context}"
        elif kwargs:
            prompt += f"\n\nContext:\n{kwargs}"

        try:
            return await self._client.complete(prompt)
        except Exception as e:
            raise PepperPyError(f"Analysis failed: {e}", cause=e)

    async def evaluate(
        self,
        results: str,
        confidence: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> AIResponse:
        """Evaluate analysis results with structured prompt.

        Args:
            results: Analysis results to evaluate
            confidence: Optional confidence level
            context: Optional evaluation context
            **kwargs: Additional arguments for evaluation

        Returns:
            AIResponse: Evaluation results

        Raises:
            PepperPyError: If evaluation fails
            RuntimeError: If agent is not initialized
        """
        self._ensure_initialized()
        prompt = (
            f"As a data analyst with the role of {self.config.role}, "
            f"please evaluate these analysis results:\n\n{results}\n\n"
            "Include:\n"
            "- Result validation\n"
            "- Confidence assessment\n"
            "- Potential biases\n"
            "- Next steps"
        )

        if confidence:
            prompt += f"\n\nConfidence level: {confidence}"

        if context:
            prompt += f"\n\nContext:\n{context}"
        elif kwargs:
            prompt += f"\n\nContext:\n{kwargs}"

        try:
            return await self._client.complete(prompt)
        except Exception as e:
            raise PepperPyError(f"Evaluation failed: {e}", cause=e)

    async def cleanup(self) -> None:
        """Cleanup agent resources."""
        if self._client.is_initialized:
            await self._client.cleanup()
            self._initialized = False


class DataAnalystAgent(AnalysisAgent):
    """Data analyst agent implementation"""

    async def analyze(self, data: str, **kwargs: Any) -> AIResponse:
        """Analyze data with structured prompt"""
        self._ensure_initialized()
        prompt = (
            f"As a data analyst with the role of {self.config.role}, "
            f"please analyze this data:\n\n{data}\n\n"
            "Include:\n"
            "- Statistical analysis\n"
            "- Key insights\n"
            "- Data patterns\n"
            "- Recommendations"
        )

        if kwargs:
            prompt += f"\n\nContext:\n{kwargs}"

        try:
            return await self._client.complete(prompt)
        except Exception as e:
            raise PepperPyError(f"Analysis failed: {e}", cause=e)

    async def evaluate(self, results: str, **kwargs: Any) -> AIResponse:
        """Evaluate analysis results with structured prompt"""
        self._ensure_initialized()
        prompt = (
            f"As a data analyst with the role of {self.config.role}, "
            f"please evaluate these analysis results:\n\n{results}\n\n"
            "Include:\n"
            "- Result validation\n"
            "- Confidence assessment\n"
            "- Potential biases\n"
            "- Next steps"
        )

        if kwargs:
            prompt += f"\n\nContext:\n{kwargs}"

        try:
            return await self._client.complete(prompt)
        except Exception as e:
            raise PepperPyError(f"Evaluation failed: {e}", cause=e)


class IntegrationAgent(BaseAgent):
    """Integration agent implementation"""

    async def execute(self, task: str, **kwargs: Any) -> AIResponse:
        """Execute integration task"""
        return await self.integrate(task, **kwargs)

    async def integrate(self, task: str, **kwargs: Any) -> AIResponse:
        """Integrate systems.

        Args:
            task: Integration task description
            **kwargs: Additional arguments for integration

        Returns:
            AIResponse: Integration results

        Raises:
            PepperPyError: If integration fails
            RuntimeError: If agent is not initialized
        """
        self._ensure_initialized()
        prompt = (
            f"As a systems integrator with the role of {self.config.role}, "
            f"please integrate:\n\n{task}\n\n"
            "Include:\n"
            "- Integration steps\n"
            "- Data mapping\n"
            "- Error handling\n"
            "- Testing plan"
        )

        if kwargs:
            prompt += f"\n\nContext:\n{kwargs}"

        try:
            return await self._client.complete(prompt)
        except Exception as e:
            raise PepperPyError(f"Integration failed: {e}", cause=e)
