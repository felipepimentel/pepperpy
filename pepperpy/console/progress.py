from typing import Iterable, Optional, Any, Union, Callable, Dict
from dataclasses import dataclass
from contextlib import contextmanager
import time
from rich.progress import (
    Progress, TextColumn, BarColumn, TimeElapsedColumn,
    TimeRemainingColumn, SpinnerColumn, TaskProgressColumn
)
from tqdm.auto import tqdm

@dataclass
class ProgressConfig:
    """Configuração para barras de progresso."""
    style: str = "rich"  # rich, tqdm, or minimal
    spinner: str = "dots"
    show_speed: bool = True
    show_eta: bool = True
    show_percentage: bool = True
    transient: bool = False
    refresh_per_second: int = 10
    on_start: Optional[Callable] = None
    on_complete: Optional[Callable] = None
    on_error: Optional[Callable] = None

@dataclass
class TaskConfig:
    """Configuração para tarefa individual."""
    description: str
    total: Optional[int] = None
    start_message: Optional[str] = None
    complete_message: Optional[str] = None
    error_message: Optional[str] = None
    show_eta: bool = True
    show_speed: bool = True

class ProgressBar:
    """Sistema unificado de progresso."""
    
    def __init__(self, config: Optional[ProgressConfig] = None):
        self.config = config or ProgressConfig()
    
    def create_progress(self) -> Progress:
        """Cria instância de Progress com configuração atual."""
        columns = [
            SpinnerColumn(spinner_name=self.config.spinner),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
        ]
        
        if self.config.show_speed:
            columns.append(TextColumn("[progress.speed]{task.speed:>.2f}it/s"))
        if self.config.show_eta:
            columns.append(TimeRemainingColumn())
            
        return Progress(*columns, transient=self.config.transient)
    
    @contextmanager
    def task_group(self):
        """Gerencia múltiplas tarefas relacionadas."""
        progress = self.create_progress()
        with progress:
            yield TaskGroup(progress, self.config)
            
class TaskGroup:
    """Gerenciador de grupo de tarefas."""
    
    def __init__(self, progress: Progress, config: ProgressConfig):
        self.progress = progress
        self.config = config
        self.tasks: Dict[str, Dict[str, Any]] = {}
    
    def add_task(self, name: str, config: Optional[TaskConfig] = None) -> str:
        """Adiciona nova tarefa com configuração específica."""
        cfg = config or TaskConfig(description=name)
        
        if cfg.start_message:
            self.progress.console.print(cfg.start_message)
            
        task_id = self.progress.add_task(
            cfg.description,
            total=cfg.total,
            show_eta=cfg.show_eta,
            show_speed=cfg.show_speed
        )
        
        self.tasks[name] = {
            "id": task_id,
            "config": cfg,
            "started": time.time()
        }
        return task_id
    
    def complete_task(self, name: str):
        """Marca tarefa como completa."""
        if task := self.tasks.get(name):
            task_id = task["id"]
            config = task["config"]
            self.progress.update(task_id, completed=True)
            
            if config.complete_message:
                elapsed = time.time() - task["started"]
                msg = config.complete_message.format(
                    elapsed=f"{elapsed:.2f}s"
                )
                self.progress.console.print(msg)
                
    def error_task(self, name: str, error: Exception):
        """Marca tarefa com erro."""
        if task := self.tasks.get(name):
            config = task["config"]
            if config.error_message:
                self.progress.console.print(
                    config.error_message.format(error=str(error)),
                    style="error"
                )
    
    def iterate(
        self,
        iterable: Iterable,
        description: Optional[str] = None,
        total: Optional[int] = None,
        process_func: Optional[Callable] = None
    ) -> Iterable:
        """Iterador com progresso e processamento opcional."""
        if self.config.style == "tqdm":
            with tqdm(
                iterable,
                desc=description,
                total=total,
                dynamic_ncols=True
            ) as pbar:
                for item in pbar:
                    yield process_func(item) if process_func else item
                    
        else:
            with self.task_group() as update:
                for item in iterable:
                    yield process_func(item) if process_func else item
                    update(item)
    
    @contextmanager
    def batch(
        self,
        total: int,
        batch_size: int,
        description: Optional[str] = None
    ):
        """Progresso para processamento em batch."""
        with self.task_group() as update:
            def process_batch(items: list):
                update(len(items))
                return items
            yield process_batch 