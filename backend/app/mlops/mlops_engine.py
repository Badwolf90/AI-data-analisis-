import os
import joblib
import json
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timezone
from scipy.stats import ks_2samp

from app.ml_engine.config import ml_config
from app.ml_engine.pipeline import ProductionPipeline
from app.core.logging import logger

try:
    import mlflow
    import mlflow.sklearn
    from mlflow.tracking import MlflowClient
except ImportError:
    mlflow = None
    MlflowClient = None


class DataDriftDetector:
    """
    Statistical Data Drift Detector.
    Uses Kolmogorov-Smirnov (KS-test) for numeric features and Population Stability Index (PSI)
    to detect feature distribution shifts between Baseline (Train Data) and Current (Inference Data).
    """

    @staticmethod
    def calculate_psi(baseline: np.ndarray, current: np.ndarray, num_bins: int = 10) -> float:
        """Calculates Population Stability Index (PSI). PSI > 0.2 indicates significant drift."""
        try:
            baseline = baseline[~np.isnan(baseline)]
            current = current[~np.isnan(current)]
            if len(baseline) == 0 or len(current) == 0:
                return 0.0

            quantiles = np.linspace(0, 100, num_bins + 1)
            bins = np.percentile(baseline, quantiles)
            bins = np.unique(bins)
            if len(bins) < 2:
                return 0.0

            bins[0] = -np.inf
            bins[-1] = np.inf

            base_counts, _ = np.histogram(baseline, bins=bins)
            curr_counts, _ = np.histogram(current, bins=bins)

            base_pct = base_counts / len(baseline)
            curr_pct = curr_counts / len(current)

            # Avoid zero counts
            base_pct = np.where(base_pct == 0, 0.0001, base_pct)
            curr_pct = np.where(curr_pct == 0, 0.0001, curr_pct)

            psi = np.sum((curr_pct - base_pct) * np.log(curr_pct / base_pct))
            return float(round(psi, 4))
        except Exception:
            return 0.0

    @staticmethod
    def detect_data_drift(
        df_baseline: pd.DataFrame,
        df_current: pd.DataFrame,
        ks_alpha: float = 0.05,
        psi_threshold: float = 0.20
    ) -> Dict[str, Any]:

        numeric_cols = df_baseline.select_dtypes(include=[np.number]).columns.intersection(df_current.columns)

        drifted_features = []
        feature_scores = {}

        for col in numeric_cols:
            base_vals = df_baseline[col].dropna().values
            curr_vals = df_current[col].dropna().values

            if len(base_vals) < 5 or len(curr_vals) < 5:
                continue

            # 1. Kolmogorov-Smirnov Test
            ks_stat, p_value = ks_2samp(base_vals, curr_vals)

            # 2. Population Stability Index (PSI)
            psi_score = DataDriftDetector.calculate_psi(base_vals, curr_vals)

            is_ks_drift = bool(p_value < ks_alpha)
            is_psi_drift = bool(psi_score > psi_threshold)
            is_drifted = is_ks_drift or is_psi_drift

            if is_drifted:
                drifted_features.append(col)

            feature_scores[col] = {
                "ks_statistic": float(round(ks_stat, 4)),
                "p_value": float(round(p_value, 4)),
                "psi_score": psi_score,
                "is_drifted": is_drifted,
                "drift_reason": "PSI > 0.20" if is_psi_drift else ("p-value < 0.05" if is_ks_drift else "No Drift")
            }

        drift_ratio = len(drifted_features) / len(numeric_cols) if len(numeric_cols) > 0 else 0.0
        overall_drift = drift_ratio > 0.30  # Overall drift if > 30% features drifted

        return {
            "drift_detected": overall_drift,
            "drift_ratio": round(drift_ratio, 4),
            "drifted_features_count": len(drifted_features),
            "total_features_evaluated": len(numeric_cols),
            "drifted_features": drifted_features,
            "feature_scores": feature_scores,
            "evaluated_at": datetime.now(timezone.utc).isoformat()
        }


class ModelDriftDetector:
    """
    Model Performance Decay & Concept Drift Detector.
    Monitors inference evaluation metrics against historical baseline performance.
    """

    @staticmethod
    def detect_model_drift(
        baseline_metric: float,
        current_metric: float,
        metric_name: str = "accuracy",
        allowed_decay_pct: float = 10.0
    ) -> Dict[str, Any]:

        decay = ((baseline_metric - current_metric) / baseline_metric) * 100.0 if baseline_metric > 0 else 0.0
        decay = max(0.0, float(round(decay, 2)))

        is_drifted = decay >= allowed_decay_pct

        return {
            "model_drift_detected": is_drifted,
            "metric_name": metric_name,
            "baseline_score": round(baseline_metric, 4),
            "current_score": round(current_metric, 4),
            "performance_decay_percentage": decay,
            "allowed_decay_threshold": allowed_decay_pct,
            "status": "ALERT_RETRAIN_NEEDED" if is_drifted else "HEALTHY",
            "evaluated_at": datetime.now(timezone.utc).isoformat()
        }


class MLOpsModelRegistry:
    """
    Enterprise Model Registry with Stage Transitions (Staging -> Production -> Archived)
    and Semantic Versioning.
    """

    def __init__(self, registry_file: str = "storage/artifacts/model_registry.json"):
        self.registry_file = registry_file
        os.makedirs(os.path.dirname(registry_file), exist_ok=True)
        if not os.path.exists(registry_file):
            with open(registry_file, "w") as f:
                json.dump({"models": {}}, f)

    def register_model(
        self,
        model_name: str,
        version: str,
        artifact_path: str,
        metrics: Dict[str, float],
        parameters: Dict[str, Any],
        git_commit_hash: str = "unknown"
    ) -> Dict[str, Any]:

        data = self._load()
        if model_name not in data["models"]:
            data["models"][model_name] = {"versions": []}

        version_entry = {
            "version": version,
            "stage": "Staging",
            "artifact_path": artifact_path,
            "metrics": metrics,
            "parameters": parameters,
            "git_commit_hash": git_commit_hash,
            "registered_at": datetime.now(timezone.utc).isoformat()
        }

        data["models"][model_name]["versions"].append(version_entry)
        self._save(data)
        return version_entry

    def transition_stage(self, model_name: str, version: str, new_stage: str) -> Dict[str, Any]:
        valid_stages = ["Staging", "Production", "Archived"]
        if new_stage not in valid_stages:
            raise ValueError(f"Invalid stage '{new_stage}'. Must be one of {valid_stages}")

        data = self._load()
        if model_name not in data["models"]:
            raise KeyError(f"Model '{model_name}' not found in registry.")

        updated_entry = None
        for entry in data["models"][model_name]["versions"]:
            if entry["version"] == version:
                entry["stage"] = new_stage
                updated_entry = entry
            elif new_stage == "Production" and entry["stage"] == "Production":
                # Demote previous Production model to Archived
                entry["stage"] = "Archived"

        if not updated_entry:
            raise KeyError(f"Version '{version}' not found for model '{model_name}'.")

        self._save(data)
        return updated_entry

    def get_production_model(self, model_name: str) -> Optional[Dict[str, Any]]:
        data = self._load()
        if model_name not in data["models"]:
            return None

        for entry in data["models"][model_name]["versions"]:
            if entry["stage"] == "Production":
                return entry
        return None

    def _load(self) -> Dict[str, Any]:
        with open(self.registry_file, "r") as f:
            return json.load(f)

    def _save(self, data: Dict[str, Any]):
        with open(self.registry_file, "w") as f:
            json.dump(data, f, indent=2)


class RetrainingManager:
    """
    Automated Model Retraining Manager.
    Triggers re-training pipeline when Data Drift or Model Drift is detected.
    """

    @staticmethod
    def trigger_automated_retrain(
        experiment_id: str,
        df_raw: pd.DataFrame,
        target_column: str,
        current_prod_score: float = 0.0,
        model_name: str = "production_classifier"
    ) -> Dict[str, Any]:

        logger.info(f"🔄 Triggering Automated Retraining for Experiment [{experiment_id}]...")

        # 1. Run 13-stage Production Pipeline
        pipeline = ProductionPipeline(experiment_id=experiment_id, version=f"v{int(datetime.now().timestamp())}")
        train_result = pipeline.fit_pipeline(df_raw=df_raw, target_column=target_column)

        new_score = train_result["best_score"]
        registry = MLOpsModelRegistry()

        # 2. Register new model version
        reg_entry = registry.register_model(
            model_name=model_name,
            version=train_result["version"],
            artifact_path=train_result["best_artifact_path"],
            metrics={"score": new_score},
            parameters={"best_algorithm": train_result["best_algorithm"]},
            git_commit_hash=train_result["git_commit_hash"]
        )

        # 3. Auto-promote to Production if performance improved
        promoted = False
        if new_score >= current_prod_score:
            registry.transition_stage(model_name=model_name, version=train_result["version"], new_stage="Production")
            promoted = True

        return {
            "experiment_id": experiment_id,
            "retrain_status": "COMPLETED",
            "new_model_version": train_result["version"],
            "new_model_score": new_score,
            "previous_prod_score": current_prod_score,
            "promoted_to_production": promoted,
            "best_algorithm": train_result["best_algorithm"],
            "artifact_path": train_result["best_artifact_path"]
        }
