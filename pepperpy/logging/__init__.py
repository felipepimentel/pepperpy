"""Enhanced logging system with elegant formatting and flexible configuration."""
from typing import Optional, Dict, Any, Union
from pathlib import Path
import sys
from dataclasses import dataclass, field
from datetime import datetime
import logging
from loguru import logger

@dataclass
class LogStyle:
    """Styling configuration for logs."""
    time_format: str = "YYYY-MM-DD HH:mm:ss"
    time_color: str = "green"
    level_padding: int = 8
    level_colors: Dict[str, str] = field(default_factory=lambda: {
        "DEBUG": "blue",
        "INFO": "green",
        "SUCCESS": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "red"
    })
    metadata_color: str = "cyan"
    message_same_as_level: bool = True

@dataclass
class LogConfig:
    """Configuration for logging system."""
    # Console settings
    console_enabled: bool = True
    console_level: str = "INFO"
    console_format: Optional[str] = None
    
    # File settings
    file_enabled: bool = True
    file_level: str = "DEBUG"
    log_dir: str = "logs"
    filename_template: str = "{time:YYYY-MM-DD}_app.log"
    rotation: str = "10 MB"
    retention: str = "30 days"
    compression: str = "zip"
    
    # Style settings
    style: LogStyle = field(default_factory=LogStyle)
    
    # Additional settings
    serialize: bool = False
    backtrace: bool = True
    diagnose: bool = True
    enqueue: bool = True
    
    def get_format(self) -> str:
        """Get formatted log template."""
        if self.console_format:
            return self.console_format
            
        return (
            f"<{self.style.time_color}>{{time:{self.style.time_format}}}</{self.style.time_color}> | "
            f"<level>{{level: <{self.style.level_padding}}}</level> | "
            f"<{self.style.metadata_color}>{{name}}</{self.style.metadata_color}>:"
            f"<{self.style.metadata_color}>{{function}}</{self.style.metadata_color}>:"
            f"<{self.style.metadata_color}>{{line}}</{self.style.metadata_color}> | "
            "<level>{message}</level>" if self.style.message_same_as_level else "{message}"
        )

class PeppyLogger:
    """Enhanced logger with elegant formatting and flexible configuration."""
    
    def __init__(self, name: Optional[str] = None, config: Optional[LogConfig] = None):
        self.name = name
        self.config = config or LogConfig()
        self._configure_logger()
    
    def _configure_logger(self) -> None:
        """Configure loguru logger with settings."""
        # Remove default handler
        logger.remove()
        
        # Add console handler
        if self.config.console_enabled:
            logger.add(
                sys.stderr,
                format=self.config.get_format(),
                level=self.config.console_level,
                colorize=True,
                backtrace=self.config.backtrace,
                diagnose=self.config.diagnose,
                filter=self._create_filter() if self.name else None
            )
        
        # Add file handler
        if self.config.file_enabled:
            log_dir = Path(self.config.log_dir)
            log_dir.mkdir(exist_ok=True)
            
            logger.add(
                str(log_dir / self.config.filename_template),
                format=self.config.get_format(),
                level=self.config.file_level,
                rotation=self.config.rotation,
                retention=self.config.retention,
                compression=self.config.compression,
                serialize=self.config.serialize,
                enqueue=self.config.enqueue,
                filter=self._create_filter() if self.name else None
            )
    
    def _create_filter(self) -> callable:
        """Create a filter for the logger name."""
        return lambda record: record["extra"].get("name") == self.name
    
    def bind(self, **kwargs) -> 'PeppyLogger':
        """Create a contextualized logger."""
        new_logger = PeppyLogger(self.name, self.config)
        logger.bind(**kwargs)
        return new_logger
    
    def debug(self, message: str, **kwargs) -> None:
        """Log debug message with optional fields."""
        logger.bind(name=self.name, **kwargs).debug(message)
    
    def info(self, message: str, **kwargs) -> None:
        """Log info message with optional fields."""
        logger.bind(name=self.name, **kwargs).info(message)
    
    def success(self, message: str, **kwargs) -> None:
        """Log success message with optional fields."""
        logger.bind(name=self.name, **kwargs).success(message)
    
    def warning(self, message: str, **kwargs) -> None:
        """Log warning message with optional fields."""
        logger.bind(name=self.name, **kwargs).warning(message)
    
    def error(self, message: str, **kwargs) -> None:
        """Log error message with optional fields."""
        logger.bind(name=self.name, **kwargs).error(message)
    
    def critical(self, message: str, **kwargs) -> None:
        """Log critical message with optional fields."""
        logger.bind(name=self.name, **kwargs).critical(message)
    
    def exception(self, message: str, **kwargs) -> None:
        """Log exception with traceback."""
        logger.bind(name=self.name, **kwargs).exception(message)

# Global logger instance with default configuration
peppy_logger = PeppyLogger()

def get_logger(
    name: Optional[str] = None,
    config: Optional[LogConfig] = None,
    style: Optional[LogStyle] = None,
    **kwargs
) -> PeppyLogger:
    """Get a logger instance with optional configuration."""
    if style and not config:
        config = LogConfig(style=style)
    return PeppyLogger(name, config).bind(**kwargs)

def set_level(level: Union[str, int]) -> None:
    """Set global log level."""
    logger.remove()
    peppy_logger._configure_logger()