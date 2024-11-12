"""Enhanced Markdown handler implementation"""

import re
from pathlib import Path
from typing import Any, Dict, List, Optional

import mistune
from bs4 import BeautifulSoup

from ..exceptions import FileError
from ..types import FileContent, Section, TableOfContents
from .base import BaseHandler


class EnhancedMarkdownHandler(BaseHandler):
    """Enhanced handler for Markdown files"""

    def __init__(self):
        self._parser = mistune.create_markdown(plugins=["table", "footnotes"])

    async def read(self, path: Path) -> FileContent:
        """Read Markdown file with enhanced features"""
        try:
            metadata = await self._get_metadata(path)
            content = await self._read_file(path)

            return FileContent(content=content, metadata=metadata, format="markdown")
        except Exception as e:
            raise FileError(f"Failed to read Markdown file: {str(e)}", cause=e)

    async def get_sections(self, content: str) -> List[Section]:
        """Extract sections based on headers"""
        sections = []
        current_section = None
        lines = content.split("\n")

        for line in lines:
            header_match = re.match(r"^(#{1,6})\s+(.+)$", line)
            if header_match:
                level = len(header_match.group(1))
                title = header_match.group(2)

                section = Section(title=title, level=level, content=[], subsections=[])

                if not current_section or level <= current_section.level:
                    sections.append(section)
                    current_section = section
                else:
                    current_section.subsections.append(section)
            elif current_section:
                current_section.content.append(line)

        return sections

    async def get_toc(self, content: str) -> TableOfContents:
        """Generate table of contents"""
        toc = []
        lines = content.split("\n")

        for line in lines:
            header_match = re.match(r"^(#{1,6})\s+(.+)$", line)
            if header_match:
                level = len(header_match.group(1))
                title = header_match.group(2)

                # Generate anchor
                anchor = re.sub(r"[^\w\s-]", "", title.lower())
                anchor = re.sub(r"[-\s]+", "-", anchor)

                toc.append({"title": title, "level": level, "anchor": anchor})

        return TableOfContents(items=toc)

    async def extract_links(self, content: str) -> List[Dict[str, str]]:
        """Extract all links from content"""
        html = self._parser(content)
        soup = BeautifulSoup(html, "html.parser")

        return [
            {"text": a.text, "url": a["href"], "title": a.get("title", "")}
            for a in soup.find_all("a")
        ]

    async def extract_images(self, content: str) -> List[Dict[str, str]]:
        """Extract all images from content"""
        html = self._parser(content)
        soup = BeautifulSoup(html, "html.parser")

        return [
            {"alt": img.get("alt", ""), "src": img["src"], "title": img.get("title", "")}
            for img in soup.find_all("img")
        ]

    async def extract_code_blocks(
        self, content: str, language: Optional[str] = None
    ) -> List[Dict[str, str]]:
        """Extract code blocks with optional language filter"""
        blocks = []
        pattern = r"```(\w+)?\n(.*?)\n```"

        for match in re.finditer(pattern, content, re.DOTALL):
            block_lang = match.group(1) or ""
            if not language or block_lang == language:
                blocks.append({"language": block_lang, "code": match.group(2)})

        return blocks

    async def extract_metadata(self, content: str) -> Dict[str, Any]:
        """Extract YAML front matter"""
        import yaml

        match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
        if match:
            try:
                return yaml.safe_load(match.group(1))
            except Exception:
                pass
        return {}

    async def search_text(
        self, content: str, query: str, context_lines: int = 2
    ) -> List[Dict[str, Any]]:
        """Search text with context"""
        results = []
        lines = content.split("\n")

        for i, line in enumerate(lines):
            if query.lower() in line.lower():
                start = max(0, i - context_lines)
                end = min(len(lines), i + context_lines + 1)

                results.append({"line_number": i + 1, "line": line, "context": lines[start:end]})

        return results

    async def convert_to_html(self, content: str, **kwargs) -> str:
        """Convert Markdown to HTML with options"""
        return self._parser(content)

    async def create_section(self, title: str, level: int, content: str) -> str:
        """Create a new section"""
        return f"{'#' * level} {title}\n\n{content}"

    async def merge_files(self, paths: List[Path], separator: str = "\n---\n") -> str:
        """Merge multiple Markdown files"""
        contents = []
        for path in paths:
            content = await self._read_file(path)
            contents.append(content)
        return separator.join(contents)
