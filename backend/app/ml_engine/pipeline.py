import os
import joblib
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Tuple

from sklearn.model_selection import train_test_split

from app.ml_engine.config import ml_config
from app.ml_engine.data import DataLoader, DataValidator
from app.ml_engine.preprocessing import DataCleaner, DataEncoder, DataScaler
from app.ml_engine.features import FeatureEngineer, FeatureSelector
from app.ml_engine.models import ModelFactory, ModelEvaluator
from app.ml_engine.tuning import OptunaHyperparameterTuner
from app.ml_engine.xai import SHAPExplainer, LIMEExplainer
from app.ml_engine.tracking import MLflowTracker


class MachineLearningPipeline:
    def __init__(self, experiment_id: str, task_type: str = "CLASSIFICATION"):
        self.experiment_id = experiment_id
        self.task_type = task_type
        self.cleaner = DataCleaner()
        self.encoder = DataEncoder()
        self.scaler = DataScaler(method="standard")
        self.selector = FeatureSelector()
        self.tracker = MLflowTracker()

    def run(
        self,
        file_path: str,
        target_column: str,
        algorithms: List[str] = None,
        tune_hyperparams: bool = True
    ) -> Dict[str, Any]:
        
        # Stage 1: Upload & Load Dataset
        df_raw = DataLoader.load(file_path)

        # Stage 2: Validation
        val_summary = DataValidator.validate(df_raw, target_column)
        if not val_summary["is_valid"]:
            raise ValueError("Dataset failed validation check.")

        # Stage 3: Data Cleaning
        df_clean = self.cleaner.fit_transform(df_raw)

        # Separate Features X and Target y
        X = df_clean.drop(columns=[target_column])
        y = df_clean[target_column]

        # Stage 4: Encoding
        X_encoded = self.encoder.fit_transform(X)
        if y.dtype == object:
            y = pd.Series(self.encoder.fit_transform(pd.DataFrame({target_column: y}))[target_column])

        # Stage 5: Scaling
        X_scaled = self.scaler.fit_transform(X_encoded)

        # Stage 6: Feature Engineering
        X_eng = FeatureEngineer.add_interaction_features(X_scaled)

        # Stage 7: Feature Selection
        X_selected = self.selector.fit_transform(X_eng)

        # Stage 8: Train-Test Split
        X_train, X_test, y_train, y_test = train_test_split(
            X_selected, y, test_size=ml_config.default_test_size, random_state=ml_config.random_state
        )

        # Select Algorithms
        supported = ModelFactory.get_supported_algorithms()
        if not algorithms:
            algorithms = supported
        else:
            algorithms = [algo for algo in algorithms if algo in supported]

        leaderboard = []
        trained_models = {}

        # Stage 9, 10, 11, 12, 13, 15, 16: Optimization, Training, Evaluation, XAI & Versioning
        for algo in algorithms:
            params = {}
            if tune_hyperparams:
                tuner = OptunaHyperparameterTuner(self.task_type, n_trials=5)
                best_params, _ = tuner.tune_algorithm(algo, X_train, y_train)
                params.update(best_params)

            model = ModelFactory.create_model(algo, self.task_type, ml_config.random_state, **params)
            model.fit(X_train, y_train)

            # Stage 13: Evaluation
            metrics = ModelEvaluator.evaluate(model, X_test, y_test, self.task_type)

            # Stage 14: Explainable AI (SHAP Global)
            shap_dict = SHAPExplainer.explain_global(model, X_test.head(50))

            # Stage 16: Model Saving & MLflow Versioning
            artifact_filename = f"{self.experiment_id}_{algo}.joblib"
            artifact_path = os.path.join(ml_config.artifact_storage_path, artifact_filename)
            tracking_uri = self.tracker.log_run(f"{self.experiment_id}_{algo}", params, metrics, model, artifact_path)

            score = metrics.get("accuracy", metrics.get("r2_score", 0.0))
            leaderboard.append({
                "algorithm": algo,
                "hyperparameters": params,
                "metrics": metrics,
                "score": score,
                "artifact_path": artifact_path,
                "tracking_uri": tracking_uri,
                "shap_summary": shap_dict,
                "model_obj": model
            })

        # Rank Leaderboard
        leaderboard.sort(key=lambda x: x["score"], reverse=True)
        best_entry = leaderboard[0]

        return {
            "experiment_id": self.experiment_id,
            "best_algorithm": best_entry["algorithm"],
            "best_score": best_entry["score"],
            "leaderboard": [
                {
                    "algorithm": item["algorithm"],
                    "metrics": item["metrics"],
                    "is_best": (item["algorithm"] == best_entry["algorithm"]),
                    "artifact_path": item["artifact_path"]
                } for item in leaderboard
            ],
            "best_model_details": best_entry
        }
