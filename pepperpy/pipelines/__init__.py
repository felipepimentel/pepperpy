"""Document processing pipelines"""

import asyncio
from pathlib import Path
from typing import Any

from pepperpy.core.exceptions import ValidationError

from .epub import EPUBPipeline
from .types import InputType, OutputType, PipelineConfig, PipelineResult

__all__ = [
    "InputType",
    "OutputType",
    "PipelineConfig",
    "PipelineResult",
    "ValidationError",
    "process_document",
    "process_document_sync",
]


async def process_document(
    input_path: Path,
    input_type: InputType | str,
    output_type: OutputType | str = OutputType.MARKDOWN,
    **kwargs: Any,
) -> PipelineResult:
    """
    Process document with appropriate pipeline

    Example:
        ```python
        from pepperpy.pipelines import process_document, InputType

        result = await process_document(
            "book.epub",
            InputType.EPUB,
            output_dir="analysis",
        )
        print(f"Analysis saved to: {result.output_path}")
        ```
    """
    # Convert string types if needed
    if isinstance(input_type, str):
        input_type = InputType(input_type)
    if isinstance(output_type, str):
        output_type = OutputType(output_type)

    # Create pipeline config
    config = PipelineConfig(
        input_type=input_type,
        output_type=output_type,
        **kwargs,
    )

    # Select appropriate pipeline
    pipeline_class = {
        InputType.EPUB: EPUBPipeline,
        # Add more pipelines here
    }.get(input_type)

    if not pipeline_class:
        raise ValueError(f"Unsupported input type: {input_type}")

    # Process document
    pipeline = pipeline_class(config)
    async with pipeline:
        return await pipeline.process(input_path)


def process_document_sync(
    input_path: Path | str,
    input_type: InputType | str,
    output_type: OutputType | str = OutputType.MARKDOWN,
    **kwargs: Any,
) -> PipelineResult:
    """
    Synchronous version of process_document

    Example:
        ```python
        from pepperpy.pipelines import process_document_sync

        result = process_document_sync(
            "book.epub",
            "epub",
            output_dir="analysis",
        )
        print(f"Analysis saved to: {result.output_path}")
        ```
    """
    if isinstance(input_path, str):
        input_path = Path(input_path)

    return asyncio.run(process_document(input_path, input_type, output_type, **kwargs))
