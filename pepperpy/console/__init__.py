"""Enhanced console capabilities using Rich."""
from typing import Any, Optional, List, Dict, Union
from dataclasses import dataclass, field
from contextlib import contextmanager
import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.syntax import Syntax
from rich.markdown import Markdown
from rich.tree import Tree
from rich.prompt import Prompt, Confirm
from rich.style import Style

@dataclass
class ConsoleConfig:
    """Configuration for console output."""
    theme: Dict[str, Style] = field(default_factory=lambda: {
        "info": Style(color="cyan"),
        "success": Style(color="green"),
        "warning": Style(color="yellow"),
        "error": Style(color="red"),
        "title": Style(color="blue", bold=True),
    })
    width: Optional[int] = None
    record: bool = False
    record_path: Optional[Path] = None
    highlight: bool = True
    markup: bool = True
    emoji: bool = True

class PeppyConsole:
    """Enhanced console with rich formatting and utilities."""
    
    def __init__(self, config: Optional[ConsoleConfig] = None):
        self.config = config or ConsoleConfig()
        self.console = Console(
            width=self.config.width,
            record=self.config.record,
            markup=self.config.markup,
            emoji=self.config.emoji,
            highlight=self.config.highlight
        )
        
    def print(self, *objects: Any, style: Optional[str] = None, **kwargs):
        """Print objects with optional styling."""
        style = self.config.theme.get(style, style)
        self.console.print(*objects, style=style, **kwargs)
    
    def info(self, message: str, **kwargs):
        """Print info message."""
        self.print(f"ℹ️  {message}", style="info", **kwargs)
    
    def success(self, message: str, **kwargs):
        """Print success message."""
        self.print(f"✅ {message}", style="success", **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Print warning message."""
        self.print(f"⚠️  {message}", style="warning", **kwargs)
    
    def error(self, message: str, **kwargs):
        """Print error message."""
        self.print(f"❌ {message}", style="error", **kwargs)
    
    def title(self, text: str, **kwargs):
        """Print title."""
        self.print(f"\n{text}\n", style="title", **kwargs)
    
    def table(
        self,
        data: List[Dict[str, Any]],
        title: Optional[str] = None,
        **kwargs
    ) -> None:
        """Create and print a table from data."""
        if not data:
            return
            
        table = Table(title=title, **kwargs)
        
        # Add columns
        for column in data[0].keys():
            table.add_column(str(column))
        
        # Add rows
        for row in data:
            table.add_row(*[str(value) for value in row.values()])
        
        self.console.print(table)
    
    def panel(
        self,
        content: Any,
        title: Optional[str] = None,
        style: Optional[str] = None,
        **kwargs
    ):
        """Print content in a panel."""
        style = self.config.theme.get(style, style)
        self.console.print(Panel(content, title=title, style=style, **kwargs))
    
    def code(
        self,
        code: str,
        language: str = "python",
        line_numbers: bool = True,
        **kwargs
    ):
        """Print syntax-highlighted code."""
        syntax = Syntax(
            code,
            language,
            line_numbers=line_numbers,
            theme="monokai",
            **kwargs
        )
        self.console.print(syntax)
    
    def markdown(self, text: str, **kwargs):
        """Print markdown-formatted text."""
        md = Markdown(text)
        self.console.print(md, **kwargs)
    
    def tree(self, data: Dict[str, Any], title: Optional[str] = None) -> None:
        """Print tree structure from dictionary."""
        tree = Tree(title or "Root")
        
        def add_to_tree(node: Tree, items: Dict[str, Any]):
            for key, value in items.items():
                if isinstance(value, dict):
                    branch = node.add(key)
                    add_to_tree(branch, value)
                else:
                    node.add(f"{key}: {value}")
        
        add_to_tree(tree, data)
        self.console.print(tree)
    
    @contextmanager
    def progress(
        self,
        description: str = "Processing",
        total: Optional[int] = None
    ):
        """Context manager for progress tracking."""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=self.console
        ) as progress:
            task = progress.add_task(description, total=total)
            yield lambda n=1: progress.update(task, advance=n)
    
    def prompt(
        self,
        message: str,
        default: Optional[str] = None,
        password: bool = False,
        **kwargs
    ) -> str:
        """Get user input with optional default value."""
        return Prompt.ask(
            message,
            console=self.console,
            default=default,
            password=password,
            **kwargs
        )
    
    def confirm(
        self,
        message: str,
        default: bool = True,
        **kwargs
    ) -> bool:
        """Get yes/no confirmation from user."""
        return Confirm.ask(
            message,
            console=self.console,
            default=default,
            **kwargs
        )
    
    def save_record(self, path: Optional[Path] = None):
        """Save recorded output to file."""
        if not self.config.record:
            raise ValueError("Console recording not enabled")
            
        path = path or self.config.record_path
        if not path:
            raise ValueError("No record path specified")
            
        self.console.save_html(path)

# Global console instance with default configuration
console = PeppyConsole()

# Convenience functions
def print_message(*args, **kwargs):
    """Print message with rich formatting."""
    console.print(*args, **kwargs)

def print_table(data: List[Dict[str, Any]], **kwargs):
    """Print table from data."""
    console.table(data, **kwargs)

def print_code(code: str, **kwargs):
    """Print syntax-highlighted code."""
    console.code(code, **kwargs)

def print_markdown(text: str, **kwargs):
    """Print markdown-formatted text."""
    console.markdown(text, **kwargs)

def get_input(message: str, **kwargs) -> str:
    """Get user input."""
    return console.prompt(message, **kwargs)

def get_confirmation(message: str, **kwargs) -> bool:
    """Get yes/no confirmation."""
    return console.confirm(message, **kwargs) 