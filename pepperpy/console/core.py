from typing import Any, Optional, Sequence, Union, List, Dict
from rich.console import Console as RichConsole
from rich.theme import Theme
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax
from rich.tree import Tree
from rich.markdown import Markdown
from rich.prompt import Prompt, Confirm
from rich.layout import Layout
from rich.live import Live
from rich.columns import Columns
from contextlib import contextmanager

class Console:
    """Interface unificada para recursos de console."""
    
    def __init__(self, theme: Optional[dict] = None):
        self._theme = Theme({
            "info": "cyan",
            "success": "green",
            "warning": "yellow",
            "error": "red bold",
            "title": "blue bold",
            "highlight": "magenta",
            "muted": "dim",
            "link": "blue underline",
            "header": "bold cyan",
            "accent": "magenta bold",
            **(theme or {})
        })
        self._console = RichConsole(theme=self._theme)
    
    def print(self, *objects: Any, style: Optional[str] = None, **kwargs) -> None:
        """Print estilizado com suporte a markdown e syntax highlighting."""
        for obj in objects:
            if isinstance(obj, str) and (obj.startswith("```") or obj.startswith("#")):
                self._console.print(Markdown(obj), **kwargs)
            else:
                self._console.print(obj, style=style, **kwargs)
    
    def table(
        self,
        data: Sequence[dict],
        title: Optional[str] = None,
        columns: Optional[List[str]] = None,
        style: Optional[dict] = None,
        expand: bool = False
    ) -> None:
        """Tabela rica com customização avançada."""
        if not data:
            return
            
        table = Table(
            title=title,
            show_header=True,
            header_style="bold blue",
            border_style="blue",
            expand=expand,
            **style or {}
        )
        
        cols = columns or list(data[0].keys())
        for col in cols:
            table.add_column(str(col), justify="left")
            
        for row in data:
            values = [str(row.get(col, "")) for col in cols]
            table.add_row(*values)
            
        self._console.print(table)
    
    def tree(self, data: Union[dict, list], title: Optional[str] = None) -> None:
        """Visualização em árvore para dados hierárquicos."""
        tree = Tree(title or "Data", style="blue")
        
        def add_node(node: Any, data: Any):
            if isinstance(data, dict):
                for k, v in data.items():
                    child = node.add(f"[bold]{k}[/]")
                    add_node(child, v)
            elif isinstance(data, list):
                for item in data:
                    child = node.add("•")
                    add_node(child, item)
            else:
                node.add(str(data))
        
        add_node(tree, data)
        self._console.print(tree)
    
    @contextmanager
    def live_table(self, columns: List[str], **kwargs):
        """Tabela com atualização em tempo real."""
        table = Table(*columns, **kwargs)
        with Live(table, refresh_per_second=4) as live:
            yield lambda *values: table.add_row(*map(str, values))
    
    def prompt_dict(self, fields: Dict[str, Any]) -> Dict[str, Any]:
        """Prompt interativo para dicionário de valores."""
        result = {}
        for key, default in fields.items():
            if isinstance(default, bool):
                result[key] = Confirm.ask(f"{key}?", default=default)
            elif isinstance(default, (list, tuple)):
                result[key] = Prompt.ask(
                    f"{key}?",
                    choices=[str(x) for x in default],
                    default=str(default[0])
                )
            else:
                result[key] = Prompt.ask(f"{key}?", default=str(default))
        return result
    
    def code_block(self, code: str, language: str = "python", line_numbers: bool = True) -> None:
        """Exibe bloco de código com syntax highlighting."""
        self._console.print(Syntax(
            code,
            language,
            line_numbers=line_numbers,
            theme="monokai"
        ))