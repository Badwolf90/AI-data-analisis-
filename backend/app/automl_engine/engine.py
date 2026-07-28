import os
import json
import joblib
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timezone
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer

from app.ml_engine.pipeline import ProductionPipeline


class DatasetTypeDetector:
    @staticmethod
    def detect(df: pd.DataFrame, target_column: Optional[str] = None) -> str:
        text_cols = [col for col in df.columns if df[col].dtype == object and df[col].str.len().mean() > 50]
        if len(text_cols) > len(df.columns) / 2:
            return "TEXT"

        datetime_cols = [col for col in df.columns if pd.api.types.is_datetime64_any_dtype(df[col]) or "date" in col.lower() or "time" in col.lower()]
        if len(datetime_cols) > 0:
            return "TIME_SERIES"

        if target_column and target_column in df.columns:
            target_series = df[target_column]
            if pd.api.types.is_numeric_dtype(target_series) and target_series.nunique() > 15:
                return "TABULAR_REGRESSION"
            return "TABULAR_CLASSIFICATION"

        return "TABULAR_CLASSIFICATION"


class TargetDetector:
    @staticmethod
    def auto_detect_target(df: pd.DataFrame) -> str:
        target_keywords = ["target", "label", "class", "y", "output", "outcome", "survived", "price", "status"]
        for col in df.columns:
            if col.lower() in target_keywords:
                return col
        return df.columns[-1]


class AutoPreprocessor:
    def __init__(self):
        self.num_imputer = SimpleImputer(strategy="median")
        self.cat_imputer = SimpleImputer(strategy="most_frequent")
        self.scaler = StandardScaler()
        self.label_encoders: Dict[str, LabelEncoder] = {}

    def auto_preprocess(self, df: pd.DataFrame, target_column: str) -> Tuple[pd.DataFrame, pd.Series, str]:
        df_proc = df.copy()
        y_raw = df_proc[target_column]
        X_raw = df_proc.drop(columns=[target_column])

        if pd.api.types.is_numeric_dtype(y_raw) and y_raw.nunique() > 15:
            task_type = "REGRESSION"
            y = y_raw.fillna(y_raw.median())
        else:
            task_type = "CLASSIFICATION"
            le_target = LabelEncoder()
            y = pd.Series(le_target.fit_transform(y_raw.astype(str)))

        num_cols = X_raw.select_dtypes(include=[np.number]).columns
        cat_cols = X_raw.select_dtypes(exclude=[np.number]).columns

        if len(num_cols) > 0:
            X_raw[num_cols] = self.num_imputer.fit_transform(X_raw[num_cols])
        if len(cat_cols) > 0:
            X_raw[cat_cols] = self.cat_imputer.fit_transform(X_raw[cat_cols].astype(str))

        for col in cat_cols:
            le = LabelEncoder()
            X_raw[col] = le.fit_transform(X_raw[col].astype(str))
            self.label_encoders[col] = le

        if len(num_cols) > 0:
            X_raw[num_cols] = self.scaler.fit_transform(X_raw[num_cols])

        return X_raw, y, task_type


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
