import json
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Generator, List, Optional, Union

import yaml
from rich.console import Console as RichConsole
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm, Prompt
from rich.table import Table
from rich.theme import Theme


class Console:
    """
    Console simplificado para desenvolvimento rápido
    """

    def __init__(self):
        self.theme = Theme(
            {
                "info": "cyan",
                "warning": "yellow",
                "error": "red",
                "success": "green",
                "highlight": "magenta",
                "muted": "dim white",
                "code": "blue",
                "data": "green",
                "url": "underline cyan",
            }
        )

        self.console = RichConsole(theme=self.theme)

    # Métodos de logging melhorados e práticos
    def log(self, message: str, style: Optional[str] = None) -> None:
        """Log com timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.console.print(f"[muted]{timestamp}[/muted] {message}", style=style)

    def info(self, message: str) -> None:
        self.log(f"ℹ {message}", style="info")

    def success(self, message: str) -> None:
        self.log(f"✓ {message}", style="success")

    def warning(self, message: str) -> None:
        self.log(f"⚠ {message}", style="warning")

    def error(self, message: str) -> None:
        self.log(f"✗ {message}", style="error")

    # Entrada de dados simplificada
    def ask(
        self,
        message: str,
        choices: Optional[List[str]] = None,
        default: Optional[str] = None,
        password: bool = False,
    ) -> str:
        return Prompt.ask(
            message,
            choices=choices,
            default=default,
            password=password,
            console=self.console,
        )

    def confirm(self, message: str, default: bool = True) -> bool:
        return Confirm.ask(message, default=default, console=self.console)

    # Utilitários práticos
    def clear(self) -> None:
        """Limpa a tela"""
        self.console.clear()

    def title(self, text: str) -> None:
        """Exibe título destacado"""
        self.console.print(f"\n[bold]{text}[/bold]\n")

    def divider(self) -> None:
        """Exibe linha divisória"""
        self.console.print("─" * 40)

    # Exibição de dados
    def show(self, data: Any, title: Optional[str] = None) -> None:
        """Exibe dados de forma inteligente"""
        if isinstance(data, (dict, list)):
            self.show_table(data, title)
        elif isinstance(data, str) and (data.startswith("{") or data.startswith("[")):
            self.show_json(data, title)
        else:
            self.console.print(str(data))

    def show_table(self, data: Union[Dict, List], title: Optional[str] = None) -> None:
        """Exibe dados em formato tabular"""
        table = Table(title=title)

        if isinstance(data, dict):
            table.add_column("Key")
            table.add_column("Value")
            for k, v in data.items():
                table.add_row(str(k), str(v))
        elif isinstance(data, list) and data and isinstance(data[0], dict):
            # Lista de dicionários
            headers = list(data[0].keys())
            for h in headers:
                table.add_column(h)
            for item in data:
                table.add_row(*[str(item.get(h, "")) for h in headers])
        else:
            # Lista simples
            table.add_column("Value")
            for item in data:
                table.add_row(str(item))

        self.console.print(table)

    def show_json(self, data: Union[str, Dict], title: Optional[str] = None) -> None:
        """Exibe JSON formatado"""
        if isinstance(data, str):
            data = json.loads(data)
        self.console.print(json.dumps(data, indent=2))

    # Progress tracking simplificado
    @contextmanager
    def progress(
        self, message: str = "Processing..."
    ) -> Generator[Progress, None, None]:
        """Barra de progresso simples"""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            console=self.console,
        ) as progress:
            task = progress.add_task(message)
            yield progress
            progress.update(task, completed=True)

    # File operations
    def save_json(self, data: Any, path: Union[str, Path]) -> None:
        """Salva dados em arquivo JSON"""
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
        self.success(f"Saved to {path}")

    def load_json(self, path: Union[str, Path]) -> Any:
        """Carrega dados de arquivo JSON"""
        with open(path) as f:
            return json.load(f)

    def save_yaml(self, data: Any, path: Union[str, Path]) -> None:
        """Salva dados em arquivo YAML"""
        with open(path, "w") as f:
            yaml.dump(data, f)
        self.success(f"Saved to {path}")

    def load_yaml(self, path: Union[str, Path]) -> Any:
        """Carrega dados de arquivo YAML"""
        with open(path) as f:
            return yaml.safe_load(f)
