"""Markdown processing and generation."""
from typing import List, Dict, Any, Optional, Union
from pathlib import Path
import re
from dataclasses import dataclass
import yaml
from datetime import datetime

@dataclass
class MarkdownBlock:
    """Represents a markdown block."""
    type: str
    content: str
    level: Optional[int] = None
    metadata: Dict[str, Any] = None

class MarkdownParser:
    """Parse and process markdown content."""
    
    def __init__(self, content: str):
        self.content = content
        self.blocks = self._parse_blocks()
    
    def _parse_blocks(self) -> List[MarkdownBlock]:
        """Parse content into blocks."""
        blocks = []
        lines = self.content.split('\n')
        current_block = []
        current_type = None
        
        for line in lines:
            # Check for headers
            if line.startswith('#'):
                if current_block:
                    blocks.append(self._create_block(current_type, current_block))
                    current_block = []
                level = len(re.match(r'^#+', line).group())
                blocks.append(MarkdownBlock(
                    type='header',
                    content=line[level:].strip(),
                    level=level
                ))
                continue
            
            # Check for code blocks
            if line.startswith('```'):
                if current_type == 'code':
                    blocks.append(self._create_block(current_type, current_block))
                    current_block = []
                    current_type = None
                else:
                    current_type = 'code'
                continue
            
            # Add line to current block
            current_block.append(line)
        
        # Add remaining block
        if current_block:
            blocks.append(self._create_block(current_type or 'text', current_block))
        
        return blocks
    
    def _create_block(self, type: str, lines: List[str]) -> MarkdownBlock:
        """Create a markdown block from lines."""
        return MarkdownBlock(
            type=type,
            content='\n'.join(lines).strip()
        )
    
    def to_html(self) -> str:
        """Convert markdown to HTML."""
        html_parts = []
        for block in self.blocks:
            if block.type == 'header':
                html_parts.append(
                    f"<h{block.level}>{block.content}</h{block.level}>"
                )
            elif block.type == 'code':
                html_parts.append(
                    f"<pre><code>{block.content}</code></pre>"
                )
            else:
                html_parts.append(f"<p>{block.content}</p>")
        return '\n'.join(html_parts)

class ObsidianNote:
    """Obsidian note with frontmatter and content."""
    
    def __init__(
        self,
        title: str,
        content: str,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.title = title
        self.content = content
        self.tags = tags or []
        self.metadata = metadata or {}
        self.created = datetime.now()
        self.modified = self.created
    
    def to_markdown(self) -> str:
        """Convert note to markdown with frontmatter."""
        frontmatter = {
            'title': self.title,
            'tags': self.tags,
            'created': self.created.isoformat(),
            'modified': self.modified.isoformat(),
            **self.metadata
        }
        
        return (
            '---\n'
            f'{yaml.dump(frontmatter)}'
            '---\n\n'
            f'{self.content}'
        )
    
    @classmethod
    def from_markdown(cls, content: str) -> 'ObsidianNote':
        """Create note from markdown content."""
        # Split frontmatter and content
        parts = content.split('---', 2)
        if len(parts) < 3:
            raise ValueError("Invalid Obsidian note format")
            
        # Parse frontmatter
        frontmatter = yaml.safe_load(parts[1])
        
        return cls(
            title=frontmatter.get('title', 'Untitled'),
            content=parts[2].strip(),
            tags=frontmatter.get('tags', []),
            metadata={
                k: v for k, v in frontmatter.items()
                if k not in ['title', 'tags', 'created', 'modified']
            }
        )

class ObsidianVault:
    """Manage an Obsidian vault."""
    
    def __init__(self, path: Union[str, Path]):
        self.path = Path(path)
        self.path.mkdir(parents=True, exist_ok=True)
    
    def create_note(
        self,
        title: str,
        content: str,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> ObsidianNote:
        """Create a new note in the vault."""
        note = ObsidianNote(title, content, tags, metadata)
        
        # Create file
        file_path = self.path / f"{title.lower().replace(' ', '_')}.md"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(note.to_markdown())
            
        return note
    
    def get_note(self, title: str) -> Optional[ObsidianNote]:
        """Get a note by title."""
        file_path = self.path / f"{title.lower().replace(' ', '_')}.md"
        if not file_path.exists():
            return None
            
        with open(file_path, 'r', encoding='utf-8') as f:
            return ObsidianNote.from_markdown(f.read())
    
    def list_notes(self) -> List[str]:
        """List all notes in the vault."""
        return [
            f.stem for f in self.path.glob('*.md')
        ]
    
    def search_notes(
        self,
        query: str,
        tags: Optional[List[str]] = None
    ) -> List[ObsidianNote]:
        """Search notes by content and tags."""
        results = []
        for file_path in self.path.glob('*.md'):
            note = self.get_note(file_path.stem)
            if note:
                # Check tags if specified
                if tags and not all(tag in note.tags for tag in tags):
                    continue
                    
                # Check content
                if query.lower() in note.content.lower():
                    results.append(note)
        return results 