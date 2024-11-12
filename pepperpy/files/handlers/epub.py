"""EPUB file handler implementation"""

import re
from pathlib import Path
from typing import Any, Dict, List, Optional

import ebooklib
from bs4 import BeautifulSoup
from ebooklib import epub

from ..exceptions import FileError
from ..types import Chapter, EpubTOC, FileContent
from .base import BaseHandler


class EPUBHandler(BaseHandler):
    """Handler for EPUB files"""

    async def read(self, path: Path) -> FileContent:
        """Read EPUB file"""
        try:
            metadata = await self._get_metadata(path)
            book = epub.read_epub(str(path))

            return FileContent(content=book, metadata=metadata, format="epub")
        except Exception as e:
            raise FileError(f"Failed to read EPUB file: {str(e)}", cause=e)

    async def get_metadata(self, book: epub.EpubBook) -> Dict[str, Any]:
        """Extract EPUB metadata"""
        return {
            "title": book.title,
            "authors": book.get_metadata("DC", "creator"),
            "language": book.get_metadata("DC", "language"),
            "publisher": book.get_metadata("DC", "publisher"),
            "rights": book.get_metadata("DC", "rights"),
            "identifier": book.get_metadata("DC", "identifier"),
            "description": book.get_metadata("DC", "description"),
        }

    async def get_chapters(self, book: epub.EpubBook) -> List[Chapter]:
        """Get all chapters"""
        chapters = []

        for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
            soup = BeautifulSoup(item.content, "html.parser")

            chapter = Chapter(
                title=soup.title.string if soup.title else "",
                content=soup.get_text(),
                html_content=item.content.decode("utf-8"),
                position=len(chapters),
                metadata={"id": item.id, "file_name": item.file_name},
            )
            chapters.append(chapter)

        return chapters

    async def get_toc(self, book: epub.EpubBook) -> EpubTOC:
        """Get table of contents"""

        def process_toc(items):
            result = []
            for item in items:
                if isinstance(item, tuple):
                    title, href, children = item
                    result.append({"title": title, "href": href, "children": process_toc(children)})
            return result

        return EpubTOC(items=process_toc(book.toc))

    async def extract_images(
        self, book: epub.EpubBook, output_dir: Optional[Path] = None
    ) -> List[Dict[str, Any]]:
        """Extract all images"""
        images = []

        for item in book.get_items_of_type(ebooklib.ITEM_IMAGE):
            image_info = {
                "id": item.id,
                "file_name": item.file_name,
                "media_type": item.media_type,
                "content": item.content,
            }

            if output_dir:
                output_path = output_dir / item.file_name
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_bytes(item.content)
                image_info["path"] = output_path

            images.append(image_info)

        return images

    async def get_chapter_by_id(self, book: epub.EpubBook, chapter_id: str) -> Optional[Chapter]:
        """Get specific chapter by ID"""
        for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
            if item.id == chapter_id:
                soup = BeautifulSoup(item.content, "html.parser")
                return Chapter(
                    title=soup.title.string if soup.title else "",
                    content=soup.get_text(),
                    html_content=item.content.decode("utf-8"),
                    metadata={"id": item.id, "file_name": item.file_name},
                )
        return None

    async def search_text(self, book: epub.EpubBook, query: str) -> List[Dict[str, Any]]:
        """Search text across all chapters"""
        results = []

        for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
            soup = BeautifulSoup(item.content, "html.parser")
            text = soup.get_text()

            if query.lower() in text.lower():
                results.append(
                    {
                        "chapter_id": item.id,
                        "chapter_title": soup.title.string if soup.title else "",
                        "matches": [
                            {
                                "context": self._get_context(text, match.start(), 50),
                                "position": match.start(),
                            }
                            for match in re.finditer(query, text, re.IGNORECASE)
                        ],
                    }
                )

        return results

    async def extract_css(self, book: epub.EpubBook) -> List[Dict[str, str]]:
        """Extract all CSS stylesheets"""
        return [
            {"id": item.id, "file_name": item.file_name, "content": item.content.decode("utf-8")}
            for item in book.get_items_of_type(ebooklib.ITEM_STYLE)
        ]

    async def create_epub(
        self, title: str, chapters: List[Dict[str, str]], metadata: Optional[Dict[str, Any]] = None
    ) -> epub.EpubBook:
        """Create new EPUB book"""
        book = epub.EpubBook()
        book.set_title(title)

        if metadata:
            for key, value in metadata.items():
                book.add_metadata("DC", key, value)

        # Add chapters
        for i, chapter in enumerate(chapters):
            epub_chapter = epub.EpubHtml(
                title=chapter["title"], file_name=f"chapter_{i+1}.xhtml", content=chapter["content"]
            )
            book.add_item(epub_chapter)

        # Add navigation
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        return book

    def _get_context(self, text: str, position: int, context_size: int) -> str:
        """Get text context around position"""
        start = max(0, position - context_size)
        end = min(len(text), position + context_size)
        return text[start:end]
