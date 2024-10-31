from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from string import Template
import json

@dataclass
class PromptTemplate:
    """Template for structured prompts."""
    template: str
    input_variables: List[str]
    template_format: str = "f-string"  # or "jinja2"
    
    def format(self, **kwargs) -> str:
        """Format the template with provided variables."""
        if self.template_format == "f-string":
            return Template(self.template).safe_substitute(**kwargs)
        elif self.template_format == "jinja2":
            from jinja2 import Template as JinjaTemplate
            return JinjaTemplate(self.template).render(**kwargs)
        raise ValueError(f"Unsupported template format: {self.template_format}")

@dataclass
class QuickCommand:
    """Represents a Stackspot Quick Command."""
    name: str
    description: str
    template: PromptTemplate
    options: Dict[str, Any] = field(default_factory=dict)
    
    def execute(self, llm: Any, **kwargs) -> Any:
        """Execute the quick command with provided parameters."""
        prompt = self.template.format(**kwargs)
        return llm.quick_command(self.name, prompt, **self.options)

class TemplateRegistry:
    """Registry for prompt templates and quick commands."""
    
    def __init__(self):
        self._templates: Dict[str, PromptTemplate] = {}
        self._quick_commands: Dict[str, QuickCommand] = {}
    
    def register_template(self, name: str, template: PromptTemplate):
        """Register a prompt template."""
        self._templates[name] = template
    
    def register_quick_command(self, command: QuickCommand):
        """Register a quick command."""
        self._quick_commands[command.name] = command
    
    def get_template(self, name: str) -> Optional[PromptTemplate]:
        """Get a registered template."""
        return self._templates.get(name)
    
    def get_quick_command(self, name: str) -> Optional[QuickCommand]:
        """Get a registered quick command."""
        return self._quick_commands.get(name)
    
    def load_templates(self, path: str):
        """Load templates from a JSON file."""
        with open(path) as f:
            data = json.load(f)
            for name, template_data in data.get("templates", {}).items():
                self.register_template(
                    name,
                    PromptTemplate(**template_data)
                )
            for cmd_data in data.get("quick_commands", []):
                self.register_quick_command(QuickCommand(**cmd_data))

# Global template registry
template_registry = TemplateRegistry() 