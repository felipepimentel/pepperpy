from typing import Any, Optional

from rich.tree import Tree as RichTree


class Tree:
    """Enhanced tree component for hierarchical data"""

    def __init__(self, console):
        self._console = console
        self._tree = None

    def new(self, label: str, **kwargs) -> RichTree:
        """Create new tree with root label"""
        self._tree = RichTree(label, **kwargs)
        return self._tree

    def add(self, parent: RichTree, label: str, **kwargs) -> RichTree:
        """Add node to tree"""
        return parent.add(label, **kwargs)

    def from_dict(self, data: dict, root_label: Optional[str] = None) -> RichTree:
        """Create tree from dictionary"""
        tree = self.new(root_label or "Root")
        self._add_dict_to_tree(tree, data)
        return tree

    def _add_dict_to_tree(self, node: RichTree, data: Any) -> None:
        """Recursively add dictionary data to tree"""
        if isinstance(data, dict):
            for key, value in data.items():
                child = self.add(node, str(key))
                self._add_dict_to_tree(child, value)
        elif isinstance(data, (list, tuple)):
            for item in data:
                child = self.add(node, str(item))
                self._add_dict_to_tree(child, item)
        else:
            self.add(node, str(data))
