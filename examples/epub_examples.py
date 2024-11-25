"""EPUB examples demonstrating file handling capabilities"""

import asyncio
from pathlib import Path
from typing import cast

from pepperpy.console import Console
from pepperpy.files.handlers.epub import EPUBHandler
from pepperpy.files.manager import FileManager
from pepperpy.files.types import Book

console = Console()


async def analyze_epub_content(epub_path: str | Path) -> None:
    """Analyze EPUB content"""
    file_manager = None
    try:
        console.info("📚 Analyzing EPUB content...")

        # Initialize handlers
        epub_handler = EPUBHandler()
        file_manager = FileManager()
        await file_manager.initialize()
        file_manager.register_handler(".epub", epub_handler)

        # Convert to Path if string
        path = Path(epub_path) if isinstance(epub_path, str) else epub_path

        # Read EPUB file
        file_content = await file_manager.read_file(path)

        # Cast content to Book type
        book: Book = cast(Book, file_content.content)
        metadata = book.metadata

        # Basic analysis
        console.info(
            "Book Information:",
            content=(
                f"Title: {metadata.title}\n"
                f"Authors: {', '.join(metadata.authors)}\n"
                f"Language: {metadata.language}\n"
                f"Chapters: {len(book.chapters)}\n"
                f"Total Images: {len(book.images)}"
            ),
        )

        # Analyze chapters
        total_words = 0
        total_chars = 0

        for chapter in book.chapters:
            # Simple analysis
            words = len(chapter.content.split())
            chars = len(chapter.content)
            total_words += words
            total_chars += chars

            console.info(
                f"Chapter: {chapter.title}",
                content=(f"Words: {words}\n" f"Characters: {chars}"),
            )

        # Summary
        console.success(
            "Analysis Complete",
            content=(
                f"Total Words: {total_words}\n"
                f"Total Characters: {total_chars}\n"
                f"Average Words per Chapter: {total_words // len(book.chapters)}"
            ),
        )

    except Exception as e:
        console.error("Analysis failed", str(e))
    finally:
        if file_manager:
            await file_manager.cleanup()


async def main() -> None:
    """Run EPUB examples"""
    try:
        epub_path = Path("examples/data/sample.epub")
        await analyze_epub_content(epub_path)
    except Exception as e:
        console.error("Example failed", str(e))


if __name__ == "__main__":
    asyncio.run(main())
