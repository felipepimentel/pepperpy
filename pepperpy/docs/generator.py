"""Documentation generator for Pepperpy."""
from typing import Dict, List, Optional
import inspect
import ast
from dataclasses import dataclass
from pathlib import Path
import re

@dataclass
class ComponentDoc:
    """Documentation for a component."""
    name: str
    description: str
    methods: List[Dict[str, str]]
    examples: List[str]
    dependencies: List[str]

class DocGenerator:
    """Generate documentation for Pepperpy components."""
    
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self._docs: Dict[str, ComponentDoc] = {}
    
    def generate_docs(self) -> None:
        """Generate documentation for all components."""
        for file_path in self.base_path.rglob("*.py"):
            if file_path.name.startswith("_"):
                continue
            
            with open(file_path) as f:
                module = ast.parse(f.read())
                
            for node in ast.walk(module):
                if isinstance(node, ast.ClassDef):
                    self._process_class(node, file_path)
    
    def _process_class(self, node: ast.ClassDef, file_path: Path) -> None:
        """Process class definition for documentation."""
        doc = ast.get_docstring(node)
        if not doc:
            return
        
        methods = []
        examples = []
        dependencies = []
        
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                method_doc = ast.get_docstring(item)
                if method_doc:
                    methods.append({
                        "name": item.name,
                        "doc": method_doc
                    })
            
            # Extract examples from docstrings
            if isinstance(item, ast.Expr) and isinstance(item.value, ast.Str):
                if "Example:" in item.value.s:
                    examples.append(item.value.s)
        
        # Extract dependencies
        with open(file_path) as f:
            content = f.read()
            imports = re.findall(r"from pepperpy\.(.*?) import", content)
            dependencies.extend(imports)
        
        self._docs[node.name] = ComponentDoc(
            name=node.name,
            description=doc,
            methods=methods,
            examples=examples,
            dependencies=dependencies
        )
    
    def generate_markdown(self, output_dir: Path) -> None:
        """Generate markdown documentation."""
        output_dir.mkdir(exist_ok=True)
        
        # Generate index
        with open(output_dir / "README.md", "w") as f:
            f.write("# Pepperpy Documentation\n\n")
            f.write("## Components\n\n")
            for name, doc in self._docs.items():
                f.write(f"- [{name}]({name}.md)\n")
        
        # Generate component docs
        for name, doc in self._docs.items():
            with open(output_dir / f"{name}.md", "w") as f:
                f.write(f"# {name}\n\n")
                f.write(f"{doc.description}\n\n")
                
                if doc.dependencies:
                    f.write("## Dependencies\n\n")
                    for dep in doc.dependencies:
                        f.write(f"- pepperpy.{dep}\n")
                
                if doc.methods:
                    f.write("\n## Methods\n\n")
                    for method in doc.methods:
                        f.write(f"### {method['name']}\n\n")
                        f.write(f"{method['doc']}\n\n")
                
                if doc.examples:
                    f.write("\n## Examples\n\n")
                    for example in doc.examples:
                        f.write(f"{example}\n\n") 