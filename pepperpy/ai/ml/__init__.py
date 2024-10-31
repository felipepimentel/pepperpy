"""Machine Learning and Data Processing capabilities."""
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
import numpy as np
from sklearn.base import BaseEstimator
from ..core.config import AIConfig
from ...utils.telemetry import metrics

@dataclass
class MLConfig:
    """Configuration for ML operations."""
    model_path: Optional[str] = None
    batch_size: int = 32
    validation_split: float = 0.2
    random_seed: int = 42
    use_gpu: bool = False
    enable_caching: bool = True

class MLManager:
    """Central manager for ML operations."""
    
    def __init__(self, config: Optional[MLConfig] = None):
        self.config = config or MLConfig()
        self._models: Dict[str, BaseEstimator] = {}
        self._pipelines: Dict[str, Any] = {}
        
    def register_model(
        self,
        name: str,
        model: BaseEstimator,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Register a scikit-learn compatible model."""
        with metrics.timer("ml.register_model"):
            self._models[name] = {
                "model": model,
                "metadata": metadata or {}
            }
    
    def get_model(self, name: str) -> BaseEstimator:
        """Get a registered model."""
        if name not in self._models:
            raise KeyError(f"Model not found: {name}")
        return self._models[name]["model"]
    
    async def train(
        self,
        name: str,
        X_train: np.ndarray,
        y_train: np.ndarray,
        **kwargs
    ) -> Dict[str, Any]:
        """Train a registered model."""
        with metrics.timer("ml.train"):
            if name not in self._models:
                raise KeyError(f"Model not found: {name}")
                
            model = self._models[name]["model"]
            model.fit(X_train, y_train, **kwargs)
            
            return {
                "model": name,
                "samples": len(X_train),
                "parameters": model.get_params()
            }
    
    async def predict(
        self,
        name: str,
        X: np.ndarray,
        **kwargs
    ) -> np.ndarray:
        """Make predictions using a trained model."""
        with metrics.timer("ml.predict"):
            if name not in self._models:
                raise KeyError(f"Model not found: {name}")
                
            model = self._models[name]["model"]
            return model.predict(X, **kwargs)
    
    async def evaluate(
        self,
        name: str,
        X_test: np.ndarray,
        y_test: np.ndarray,
        metrics: List[str] = ["accuracy", "f1"],
        **kwargs
    ) -> Dict[str, float]:
        """Evaluate model performance."""
        from sklearn.metrics import (
            accuracy_score,
            f1_score,
            precision_score,
            recall_score
        )
        
        with metrics.timer("ml.evaluate"):
            if name not in self._models:
                raise KeyError(f"Model not found: {name}")
                
            model = self._models[name]["model"]
            y_pred = model.predict(X_test)
            
            results = {}
            for metric in metrics:
                if metric == "accuracy":
                    results[metric] = accuracy_score(y_test, y_pred)
                elif metric == "f1":
                    results[metric] = f1_score(y_test, y_pred, average="weighted")
                elif metric == "precision":
                    results[metric] = precision_score(y_test, y_pred, average="weighted")
                elif metric == "recall":
                    results[metric] = recall_score(y_test, y_pred, average="weighted")
                    
            return results
    
    def save_model(self, name: str, path: Optional[str] = None) -> str:
        """Save model to disk."""
        import joblib
        
        if name not in self._models:
            raise KeyError(f"Model not found: {name}")
            
        path = path or f"{name}_model.joblib"
        joblib.dump(self._models[name]["model"], path)
        return path
    
    def load_model(
        self,
        name: str,
        path: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Load model from disk."""
        import joblib
        
        model = joblib.load(path)
        self.register_model(name, model, metadata)

# Convenience functions
def create_ml_manager(config: Optional[MLConfig] = None) -> MLManager:
    """Create a new ML manager instance."""
    return MLManager(config)

def get_default_manager() -> MLManager:
    """Get or create default ML manager."""
    if not hasattr(get_default_manager, "_instance"):
        get_default_manager._instance = MLManager()
    return get_default_manager._instance 