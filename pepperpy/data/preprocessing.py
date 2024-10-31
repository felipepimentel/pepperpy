"""Text preprocessing utilities."""
from typing import List, Optional, Callable
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

@dataclass
class PreprocessingStep:
    """Represents a preprocessing step with metadata."""
    name: str
    function: Callable[[str], str]
    description: str = ""
    enabled: bool = True

class TextPreprocessor:
    """Configurable text preprocessing pipeline."""
    
    def __init__(self):
        self.steps: List[PreprocessingStep] = []
        self._initialize_default_steps()
    
    def _initialize_default_steps(self):
        """Initialize default preprocessing steps."""
        self.add_step(
            "normalize_whitespace",
            lambda text: ' '.join(text.split()),
            "Normalize whitespace characters"
        )
        
        self.add_step(
            "remove_urls",
            lambda text: re.sub(r'http\S+|www.\S+', '', text),
            "Remove URLs"
        )
        
        self.add_step(
            "remove_html",
            lambda text: re.sub(r'<[^>]+>', '', text),
            "Remove HTML tags"
        )
    
    def add_step(
        self, 
        name: str, 
        func: Callable[[str], str], 
        description: str = ""
    ):
        """Add a preprocessing step."""
        self.steps.append(PreprocessingStep(
            name=name,
            function=func,
            description=description
        ))
    
    def remove_step(self, name: str):
        """Remove a preprocessing step."""
        self.steps = [s for s in self.steps if s.name != name]
    
    def enable_step(self, name: str):
        """Enable a preprocessing step."""
        for step in self.steps:
            if step.name == name:
                step.enabled = True
    
    def disable_step(self, name: str):
        """Disable a preprocessing step."""
        for step in self.steps:
            if step.name == name:
                step.enabled = False
    
    def process(self, text: str) -> str:
        """Apply all enabled preprocessing steps."""
        for step in self.steps:
            if step.enabled:
                text = step.function(text)
        return text 