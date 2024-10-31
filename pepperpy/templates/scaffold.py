"""Project scaffolding system."""
from typing import Dict, Optional
from pathlib import Path
import shutil
import jinja2
import yaml

class ProjectScaffold:
    """Generate project structure from templates."""
    
    def __init__(self, templates_dir: Optional[str] = None):
        self.templates_dir = Path(templates_dir or Path(__file__).parent / "default")
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(self.templates_dir)),
            trim_blocks=True,
            lstrip_blocks=True
        )
    
    def create_project(
        self, 
        name: str, 
        template: str = "default",
        context: Optional[Dict] = None
    ) -> Path:
        """
        Create new project from template.
        
        Args:
            name: Project name
            template: Template name ("fastapi", "cli", "django", etc)
            context: Template variables
        """
        template_dir = self.templates_dir / template
        if not template_dir.exists():
            raise ValueError(f"Template '{template}' not found")
            
        # Create project directory
        project_dir = Path(name)
        project_dir.mkdir(exist_ok=True)
        
        context = {
            "project_name": name,
            **(context or {})
        }
        
        # Copy template files
        for src in template_dir.rglob("*"):
            if src.is_file():
                # Get relative path
                rel_path = src.relative_to(template_dir)
                
                # Process path template
                dest_path = project_dir / str(rel_path).format(**context)
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                
                if src.suffix in (".py", ".yml", ".md", ".txt", ".html"):
                    # Render template
                    template = self.env.get_template(f"{template}/{rel_path}")
                    content = template.render(**context)
                    dest_path.write_text(content)
                else:
                    # Copy binary files
                    shutil.copy2(src, dest_path)
        
        return project_dir