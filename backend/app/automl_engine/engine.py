import os
import json
import joblib
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timezone

from app.ml_engine.pipeline import ProductionPipeline


class TargetDetector:
    @staticmethod
    def auto_detect_target(df: pd.DataFrame) -> str:
        target_keywords = ["target", "label", "class", "y", "output", "outcome", "survived", "price", "status"]
        for col in df.columns:
            if col.lower() in target_keywords:
                return col
        return df.columns[-1]


class AutoMLEngine:
    def __init__(self, experiment_id: str, version: str = "v1.0.0"):
        self.experiment_id = experiment_id
        self.version = version
        self.pipeline = ProductionPipeline(experiment_id=experiment_id, version=version)

    def run_full_automl(
        self,
        df: pd.DataFrame,
        target_column: Optional[str] = None,
        n_trials_per_model: int = 5
    ) -> Dict[str, Any]:

        if not target_column or target_column not in df.columns:
            target_column = TargetDetector.auto_detect_target(df)

        result = self.pipeline.fit_pipeline(
            df_raw=df,
            target_column=target_column,
            n_trials=n_trials_per_model
        )

        return {
            "experiment_id": self.experiment_id,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "target_column": target_column,
            "task_type": result["task_type"],
            "version": result["version"],
            "git_commit_hash": result["git_commit_hash"],
            "total_samples": len(df),
            "best_algorithm": result["best_algorithm"],
            "best_score": result["best_score"],
            "best_model_path": result["best_artifact_path"],
            "leaderboard": result["leaderboard"],
            "shap_feature_importance": result["shap_summary"]
        }
