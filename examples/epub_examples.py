"""EPUB examples demonstrating file handling capabilities"""

import asyncio
from pathlib import Path

from pepperpy.console import Console
from pepperpy.files.handlers.epub import EPUBHandler
from pepperpy.files.manager import FileManager

console = Console()


async def demonstrate_epub_handling() -> None:
    """Demonstrate EPUB file handling"""
    try:
        console.info("📚 Initializing EPUB Handler...")

        # Initialize file manager and handler
        file_manager = FileManager()
        await file_manager.initialize()

        try:
            # Register EPUB handler
            epub_handler = EPUBHandler()
            file_manager.register_handler(".epub", epub_handler)

            console.info("Reading EPUB file...")

            # Example EPUB path
            epub_path = Path("examples/data/sample.epub")

            # Read EPUB content
            book = await file_manager.read_file(str(epub_path))

            # Display book information
            console.info(
                "Book Information:",
                content=(
                    f"Title: {book.metadata.title}\n"
                    f"Authors: {', '.join(book.metadata.authors)}\n"
                    f"Language: {book.metadata.language}\n"
                    f"Chapters: {len(book.chapters)}\n"
                    f"Total Images: {len(book.images)}"
                ),
            )

            # Process chapters
            for chapter in book.chapters:
                console.info(
                    f"Chapter: {chapter.title}",
                    content=f"Content length: {len(chapter.content)} chars",
                )

            console.success("EPUB processing complete!")

        finally:
            await file_manager.cleanup()

    except FileNotFoundError:
        console.error("EPUB file not found")
    except Exception as e:
        console.error("EPUB handling failed", str(e))


async def main() -> None:
    """Run EPUB examples"""
    try:
        await demonstrate_epub_handling()
    except KeyboardInterrupt:
        console.info("\nExamples finished! 👋")


if __name__ == "__main__":
    asyncio.run(main())
