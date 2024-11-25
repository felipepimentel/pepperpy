"""Tests for text analyzer module"""

import pytest

from pepperpy.ai.text.analyzer import TextAnalyzer
from pepperpy.ai.text.config import TextAnalyzerConfig
from pepperpy.ai.text.exceptions import TextAnalysisError
from pepperpy.ai.text.types import TextAnalysis


@pytest.fixture
def analyzer_config():
    """Fixture for analyzer config"""
    return TextAnalyzerConfig(
        language="en", min_length=10, max_length=1000, metadata={"environment": "test"}
    )


@pytest.fixture
def text_analyzer(analyzer_config):
    """Fixture for text analyzer"""
    return TextAnalyzer(analyzer_config)


@pytest.mark.asyncio
async def test_analyzer_initialize(text_analyzer):
    """Test analyzer initialization"""
    await text_analyzer.initialize()
    assert text_analyzer.is_initialized


@pytest.mark.asyncio
async def test_analyzer_cleanup(text_analyzer):
    """Test analyzer cleanup"""
    await text_analyzer.initialize()
    await text_analyzer.cleanup()
    assert not text_analyzer.is_initialized


@pytest.mark.asyncio
async def test_analyzer_analyze_text(text_analyzer):
    """Test text analysis"""
    await text_analyzer.initialize()

    text = "This is a test text for analysis."
    result = await text_analyzer.analyze(text)

    assert isinstance(result, TextAnalysis)
    assert result.text == text
    assert result.language == "en"
    assert result.word_count > 0
    assert result.sentence_count > 0
    assert result.complexity_score >= 0


@pytest.mark.asyncio
async def test_analyzer_analyze_empty_text(text_analyzer):
    """Test analysis with empty text"""
    await text_analyzer.initialize()

    with pytest.raises(TextAnalysisError, match="Empty text"):
        await text_analyzer.analyze("")


@pytest.mark.asyncio
async def test_analyzer_analyze_short_text(text_analyzer):
    """Test analysis with text shorter than min_length"""
    await text_analyzer.initialize()

    with pytest.raises(TextAnalysisError, match="Text too short"):
        await text_analyzer.analyze("Short")


@pytest.mark.asyncio
async def test_analyzer_analyze_long_text(text_analyzer):
    """Test analysis with text longer than max_length"""
    await text_analyzer.initialize()

    long_text = "a" * (text_analyzer.config.max_length + 1)
    with pytest.raises(TextAnalysisError, match="Text too long"):
        await text_analyzer.analyze(long_text)


@pytest.mark.asyncio
async def test_analyzer_analyze_batch(text_analyzer):
    """Test batch text analysis"""
    await text_analyzer.initialize()

    texts = [
        "This is the first test text.",
        "This is the second test text.",
        "This is the third test text.",
    ]

    results = await text_analyzer.analyze_batch(texts)

    assert len(results) == len(texts)
    for result, text in zip(results, texts):
        assert isinstance(result, TextAnalysis)
        assert result.text == text
        assert result.language == "en"
        assert result.word_count > 0
        assert result.sentence_count > 0
        assert result.complexity_score >= 0


@pytest.mark.asyncio
async def test_analyzer_analyze_batch_empty(text_analyzer):
    """Test batch analysis with empty list"""
    await text_analyzer.initialize()

    with pytest.raises(TextAnalysisError, match="Empty batch"):
        await text_analyzer.analyze_batch([])


@pytest.mark.asyncio
async def test_analyzer_analyze_batch_invalid(text_analyzer):
    """Test batch analysis with invalid texts"""
    await text_analyzer.initialize()

    texts = ["Valid text", "", "Another valid text"]

    with pytest.raises(TextAnalysisError, match="Empty text"):
        await text_analyzer.analyze_batch(texts)


@pytest.mark.asyncio
async def test_analyzer_not_initialized(text_analyzer):
    """Test error when analyzer not initialized"""
    with pytest.raises(RuntimeError, match="Analyzer not initialized"):
        await text_analyzer.analyze("test")


@pytest.mark.asyncio
async def test_analyzer_language_detection(text_analyzer):
    """Test language detection"""
    await text_analyzer.initialize()

    # English text
    en_text = "This is an English text."
    en_result = await text_analyzer.analyze(en_text)
    assert en_result.language == "en"

    # Spanish text
    es_text = "Este es un texto en español."
    es_result = await text_analyzer.analyze(es_text)
    assert es_result.language == "es"


@pytest.mark.asyncio
async def test_analyzer_complexity_score(text_analyzer):
    """Test complexity score calculation"""
    await text_analyzer.initialize()

    # Simple text
    simple_text = "The cat sat on the mat."
    simple_result = await text_analyzer.analyze(simple_text)

    # Complex text
    complex_text = (
        "The quantum mechanical properties of subatomic particles exhibit wave-particle duality."
    )
    complex_result = await text_analyzer.analyze(complex_text)

    assert complex_result.complexity_score > simple_result.complexity_score


@pytest.mark.asyncio
async def test_analyzer_custom_config():
    """Test analyzer with custom configuration"""
    config = TextAnalyzerConfig(
        language="en", min_length=20, max_length=500, metadata={"environment": "test"}
    )

    analyzer = TextAnalyzer(config)
    await analyzer.initialize()

    # Test min length
    with pytest.raises(TextAnalysisError, match="Text too short"):
        await analyzer.analyze("Short text")


@pytest.mark.asyncio
async def test_analyzer_metrics(text_analyzer):
    """Test text metrics calculation"""
    await text_analyzer.initialize()

    text = "This is a test text. It has two sentences."
    result = await text_analyzer.analyze(text)

    assert result.word_count == 9
    assert result.sentence_count == 2
    assert result.avg_word_length > 0
    assert result.avg_sentence_length > 0


@pytest.mark.asyncio
async def test_analyzer_special_characters(text_analyzer):
    """Test handling of special characters"""
    await text_analyzer.initialize()

    text = "Text with special chars: !@#$%^&*()"
    result = await text_analyzer.analyze(text)

    assert result.text == text
    assert result.word_count == 5  # Should ignore special chars in word count
