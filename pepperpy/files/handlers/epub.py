"""EPUB file handler implementation"""

from pathlib import Path
from typing import Any, Dict, List, Optional

from bs4 import BeautifulSoup
from ebooklib import epub

from ..exceptions import FileError
from ..types import Chapter, EpubTOC, FileContent, FileMetadata
from .base import BaseHandler


class EPUBHandler(BaseHandler):
    """Handler for EPUB files"""

    async def read(self, path: Path) -> FileContent:
        """Read EPUB file"""
        try:
            metadata = await self._get_metadata(path)
            book = epub.read_epub(str(path))

            # Extract chapters
            chapters = self._extract_chapters(book)
            toc = EpubTOC(items=chapters)

            enhanced_metadata = {
                **metadata.metadata,
                "toc": toc,
                "chapters": chapters,
            }

            return FileContent(content=book, metadata=enhanced_metadata, format="epub")
        except Exception as e:
            raise FileError(f"Failed to read EPUB file: {str(e)}", cause=e)

    async def write(
        self, path: Path, content: epub.EpubBook, metadata: Optional[Dict[str, Any]] = None
    ) -> FileMetadata:
        """Write EPUB file"""
        try:
            epub.write_epub(str(path), content)
            return await self._get_metadata(path)
        except Exception as e:
            raise FileError(f"Failed to write EPUB file: {str(e)}", cause=e)

    def _extract_chapters(self, book: epub.EpubBook) -> List[Chapter]:
        """Extract chapters from EPUB book"""
        chapters: List[Chapter] = []
        order = 0

        for item in book.get_items():
            if isinstance(item, epub.EpubHtml):
                # Parse HTML content
                soup = BeautifulSoup(item.content, "lxml")
                title = soup.find("title")
                title_text = title.text if title else item.file_name

                chapter = Chapter(
                    title=title_text,
                    content=str(soup),
                    order=order,
                    identifier=item.id,
                    metadata={
                        "file_name": item.file_name,
                        "media_type": item.media_type,
                    },
                )
                chapters.append(chapter)
                order += 1

        return chapters

    def _create_chapter(
        self,
        title: str,
        content: str,
        order: int,
        identifier: Optional[str] = None,
        level: int = 1,
    ) -> Chapter:
        """Create chapter with HTML content"""
        return Chapter(
            title=title,
            content=content,
            order=order,
            level=level,
            identifier=identifier or f"chapter_{order}",
        )

    def _add_chapter(
        self,
        book: epub.EpubBook,
        chapter: Chapter,
    ) -> None:
        """Add chapter to EPUB book"""
        epub_chapter = epub.EpubHtml(
            title=chapter.title,
            file_name=f"chapter_{chapter.order}.xhtml",
            content=chapter.content,
        )
        book.add_item(epub_chapter)
        book.spine.append(epub_chapter)
