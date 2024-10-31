"""Example of ML capabilities."""
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from pepperpy.ai.ml import create_ml_manager, MLConfig

async def demonstrate_ml():
    # Create ML manager with custom config
    config = MLConfig(
        batch_size=64,
        validation_split=0.2,
        use_gpu=True
    )
    ml = create_ml_manager(config)
    
    # Create sample data
    X = np.random.rand(100, 4)
    y = np.random.randint(0, 2, 100)
    
    # Create and register model
    model = RandomForestClassifier(n_estimators=100)
    ml.register_model(
        "rf_classifier",
        model,
        metadata={
            "type": "classifier",
            "features": ["f1", "f2", "f3", "f4"],
            "target": "binary"
        }
    )
    
    # Train model
    train_result = await ml.train(
        "rf_classifier",
        X,
        y,
        verbose=True
    )
    print(f"Training completed: {train_result}")
    
    # Make predictions
    X_new = np.random.rand(10, 4)
    predictions = await ml.predict("rf_classifier", X_new)
    print(f"Predictions: {predictions}")
    
    # Evaluate model
    metrics = await ml.evaluate(
        "rf_classifier",
        X,
        y,
        metrics=["accuracy", "f1", "precision", "recall"]
    )
    print(f"Evaluation metrics: {metrics}")
    
    # Save model
    saved_path = ml.save_model("rf_classifier", "rf_model.joblib")
    print(f"Model saved to: {saved_path}")
    
    # Load model with new name
    ml.load_model(
        "rf_classifier_loaded",
        saved_path,
        metadata={"loaded_from": saved_path}
    )

if __name__ == "__main__":
    import asyncio
    asyncio.run(demonstrate_ml()) 