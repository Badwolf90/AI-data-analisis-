import os
import joblib
from typing import Dict, Any, Optional
from app.ml_engine.config import ml_config

try:
    import mlflow
    import mlflow.sklearn
except ImportError:
    mlflow = None


class MLflowTracker:
    def __init__(self, experiment_name: str = ml_config.mlflow_experiment_name):
        self.experiment_name = experiment_name
        if mlflow is not None:
            try:
                mlflow.set_tracking_uri(ml_config.mlflow_tracking_uri)
                mlflow.set_experiment(experiment_name)
            except Exception:
                pass

    def log_run(
        self,
        run_name: str,
        params: Dict[str, Any],
        metrics: Dict[str, float],
        model,
        artifact_path: str
    ) -> str:
        # Save model locally via joblib
        joblib.dump(model, artifact_path)

        if mlflow is None:
            return artifact_path

        try:
            with mlflow.start_run(run_name=run_name):
                mlflow.log_params(params)
                mlflow.log_metrics(metrics)
                mlflow.sklearn.log_model(model, artifact_path="model")
                run_id = mlflow.active_run().info.run_id
                return f"mlflow://runs/{run_id}/model"
        except Exception:
            return artifact_path
