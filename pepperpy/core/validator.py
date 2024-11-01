"""Component validation system."""
from typing import Type, List, Dict, Any
import inspect
from dataclasses import dataclass
from .interfaces import PepperpyComponent
from .context import ExecutionContext

@dataclass
class ValidationResult:
    """Result of component validation."""
    is_valid: bool
    errors: List[str]
    warnings: List[str]

class ComponentValidator:
    """Validate Pepperpy components."""
    
    @classmethod
    def validate_component(cls, component: Type[PepperpyComponent]) -> ValidationResult:
        """Validate a component implementation."""
        errors = []
        warnings = []
        
        # Validate interface implementation
        if not issubclass(component, PepperpyComponent):
            errors.append(f"{component.__name__} must implement PepperpyComponent")
        
        # Validate required methods
        required_methods = cls._get_required_methods(PepperpyComponent)
        for method_name, method_sig in required_methods.items():
            if not hasattr(component, method_name):
                errors.append(f"Missing required method: {method_name}")
            else:
                component_method = getattr(component, method_name)
                if not cls._validate_signature(component_method, method_sig):
                    errors.append(
                        f"Invalid signature for {method_name} in {component.__name__}"
                    )
        
        # Validate docstrings
        if not component.__doc__:
            warnings.append(f"{component.__name__} missing class documentation")
        
        for method_name, method in inspect.getmembers(component, inspect.isfunction):
            if not method.__doc__ and not method_name.startswith('_'):
                warnings.append(f"Method {method_name} missing documentation")
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
    
    @staticmethod
    def _get_required_methods(interface: Type) -> Dict[str, inspect.Signature]:
        """Get required methods from interface."""
        return {
            name: inspect.signature(method)
            for name, method in inspect.getmembers(interface, inspect.isfunction)
            if not name.startswith('_')
        }
    
    @staticmethod
    def _validate_signature(
        method: callable,
        required_sig: inspect.Signature
    ) -> bool:
        """Validate method signature against required signature."""
        method_sig = inspect.signature(method)
        
        # Compare parameters
        method_params = list(method_sig.parameters.values())
        required_params = list(required_sig.parameters.values())
        
        if len(method_params) != len(required_params):
            return False
        
        for mp, rp in zip(method_params, required_params):
            if mp.kind != rp.kind:
                return False
            if mp.default != rp.default and mp.default != inspect.Parameter.empty:
                return False
        
        return True 