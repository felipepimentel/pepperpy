"""Text analyzer module"""

from typing import List, Sequence

from .config import TextAnalyzerConfig
from .exceptions import TextAnalysisError
from .types import TextAnalysis


class TextAnalyzer:
    """Text analyzer implementation"""

    def __init__(self, config: TextAnalyzerConfig) -> None:
        """Initialize analyzer"""
        self.config = config
        self._initialized = False

    @property
    def is_initialized(self) -> bool:
        """Check if analyzer is initialized"""
        return self._initialized

    async def initialize(self) -> None:
        """Initialize analyzer"""
        self._initialized = True

    async def cleanup(self) -> None:
        """Cleanup analyzer"""
        self._initialized = False

    async def analyze_batch(self, texts: Sequence[str]) -> List[TextAnalysis]:
        """Analyze multiple texts"""
        if not self._initialized:
            raise RuntimeError("Analyzer not initialized")

        if not texts:
            raise TextAnalysisError("Empty batch")

        results = []
        for text in texts:
            result = await self.analyze(text)
            results.append(result)
        return results

    async def analyze(self, text: str) -> TextAnalysis:
        """Analyze text"""
        if not self._initialized:
            raise RuntimeError("Analyzer not initialized")

        if not text:
            raise TextAnalysisError("Empty text")

        if len(text) < self.config.min_length:
            raise TextAnalysisError("Text too short")

        if len(text) > self.config.max_length:
            raise TextAnalysisError("Text too long")

        # Calculate metrics
        word_count, sentence_count, avg_word_length, avg_sentence_length = self._calculate_metrics(
            text
        )

        return TextAnalysis(
            text=text,
            language=self._detect_language(text),
            word_count=word_count,
            sentence_count=sentence_count,
            avg_word_length=avg_word_length,
            avg_sentence_length=avg_sentence_length,
            complexity_score=self._calculate_complexity(text),
        )

    def _detect_language(self, text: str) -> str:
        """Detect text language"""
        # Simple language detection based on common words
        spanish_words = {"el", "la", "es", "un", "una", "en", "español"}
        text_words = set(text.lower().split())

        if len(text_words.intersection(spanish_words)) >= 2:
            return "es"
        return "en"

    def _calculate_metrics(self, text: str) -> tuple[int, int, float, float]:
        """Calculate text metrics"""
        words = text.split()
        sentences = [s for s in text.split(".") if s.strip()]

        word_count = len(words)
        sentence_count = len(sentences)

        # Calculate averages
        total_word_length = sum(len(word) for word in words)
        avg_word_length = total_word_length / word_count if word_count > 0 else 0
        avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0

        return word_count, sentence_count, avg_word_length, avg_sentence_length

    def _calculate_complexity(self, text: str) -> float:
        """Calculate text complexity score"""
        words = text.split()
        if not words:
            return 0.0

        avg_word_length = sum(len(word) for word in words) / len(words)
        return avg_word_length * 0.1  # Simplified score
