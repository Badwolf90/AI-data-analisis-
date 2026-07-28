import os
import json
import joblib
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timezone

from sklearn.model_selection import train_test_split, StratifiedKFold, KFold, cross_validate
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder

from app.ml_engine.config import ml_config
from app.ml_engine.models import ModelFactory, ModelEvaluator
from app.ml_engine.tuning import OptunaHyperparameterTuner
from app.ml_engine.xai import SHAPExplainer
from app.ml_engine.tracking import MLflowTracker


class DatasetTypeDetector:
    @staticmethod
    def detect(df: pd.DataFrame, target_column: Optional[str] = None) -> str:
        # Check if text heavy
        text_cols = [col for col in df.columns if df[col].dtype == object and df[col].str.len().mean() > 50]
        if len(text_cols) > len(df.columns) / 2:
            return "TEXT"

        # Check datetime/time series
        datetime_cols = [col for col in df.columns if pd.api.types.is_datetime64_any_dtype(df[col]) or "date" in col.lower() or "time" in col.lower()]
        if len(datetime_cols) > 0:
            return "TIME_SERIES"

        # Determine Target column task
        if target_column and target_column in df.columns:
            target_series = df[target_column]
            if pd.api.types.is_numeric_dtype(target_series) and target_series.nunique() > 15:
                return "TABULAR_REGRESSION"
            return "TABULAR_CLASSIFICATION"

        return "TABULAR_CLASSIFICATION"


class TargetDetector:
    @staticmethod
    def auto_detect_target(df: pd.DataFrame) -> str:
        # Priority 1: Check for keywords in column names
        target_keywords = ["target", "label", "class", "y", "output", "outcome", "survived", "price", "status"]
        for col in df.columns:
            if col.lower() in target_keywords:
                return col

        # Priority 2: Pick the last column by convention
        return df.columns[-1]


class AutoPreprocessor:
    def __init__(self):
        self.num_imputer = SimpleImputer(strategy="median")
        self.cat_imputer = SimpleImputer(strategy="most_frequent")
        self.scaler = StandardScaler()
        self.label_encoders: Dict[str, LabelEncoder] = {}

    def auto_preprocess(self, df: pd.DataFrame, target_column: str) -> Tuple[pd.DataFrame, pd.Series, str]:
        df_proc = df.copy()

        # Separate X and y
        y_raw = df_proc[target_column]
        X_raw = df_proc.drop(columns=[target_column])

        # Detect Task Type (Classification vs Regression)
        if pd.api.types.is_numeric_dtype(y_raw) and y_raw.nunique() > 15:
            task_type = "REGRESSION"
            y = y_raw.fillna(y_raw.median())
        else:
            task_type = "CLASSIFICATION"
            le_target = LabelEncoder()
            y = pd.Series(le_target.fit_transform(y_raw.astype(str)))

        # Clean X
        num_cols = X_raw.select_dtypes(include=[np.number]).columns
        cat_cols = X_raw.select_dtypes(exclude=[np.number]).columns

        if len(num_cols) > 0:
            X_raw[num_cols] = self.num_imputer.fit_transform(X_raw[num_cols])
        if len(cat_cols) > 0:
            X_raw[cat_cols] = self.cat_imputer.fit_transform(X_raw[cat_cols].astype(str))

        # Encode Categorical Features
        for col in cat_cols:
            le = LabelEncoder()
            X_raw[col] = le.fit_transform(X_raw[col].astype(str))
            self.label_encoders[col] = le

        # Scale Numeric Features
        if len(num_cols) > 0:
            X_raw[num_cols] = self.scaler.fit_transform(X_raw[num_cols])

        return X_raw, y, task_type


class AutoMLEngine:
    def __init__(self, experiment_id: str):
        self.experiment_id = experiment_id
        self.preprocessor = AutoPreprocessor()
        self.tracker = MLflowTracker()

    def run_full_automl(
        self,
        df: pd.DataFrame,
        target_column: Optional[str] = None,
        n_trials_per_model: int = 5
    ) -> Dict[str, Any]:

        # Step 1: Detect Target Column if not specified
        if not target_column or target_column not in df.columns:
            target_column = TargetDetector.auto_detect_target(df)

        # Step 2: Detect Dataset Type
        dataset_type = DatasetTypeDetector.detect(df, target_column)

        # Step 3: Automatic Preprocessing
        X, y, task_type = self.preprocessor.auto_preprocess(df, target_column)

        # Step 4: Train-Test Split & Stratified K-Fold / K-Fold CV
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        cv_splitter = StratifiedKFold(n_splits=5, shuffle=True, random_state=42) if task_type == "CLASSIFICATION" else KFold(n_splits=5, shuffle=True, random_state=42)

        # Step 5: Candidate Algorithms (Minimal 10 algorithms)
        candidate_algorithms = ModelFactory.get_supported_algorithms()

        leaderboard = []

        # Step 6: Loop through algorithms (Hyperparameter Tuning, Cross Validation, Training)
        for algo in candidate_algorithms:
            # Optuna Hyperparameter Optimization
            tuner = OptunaHyperparameterTuner(task_type=task_type, n_trials=n_trials_per_model)
            best_params, cv_score = tuner.tune_algorithm(algo, X_train, y_train)

            # Fit Final Model with Best Params
            model = ModelFactory.create_model(algo, task_type=task_type, random_state=42, **best_params)
            model.fit(X_train, y_train)

            # Evaluation
            metrics = ModelEvaluator.evaluate(model, X_test, y_test, task_type=task_type)
            primary_metric = metrics.get("accuracy", metrics.get("r2_score", 0.0))

            # Explainable AI SHAP Summary
            shap_dict = SHAPExplainer.explain_global(model, X_test.head(50))

            # Save Model Artifact
            artifact_filename = f"{self.experiment_id}_{algo}.joblib"
            artifact_path = os.path.join(ml_config.artifact_storage_path, artifact_filename)
            tracking_uri = self.tracker.log_run(f"{self.experiment_id}_{algo}", best_params, metrics, model, artifact_path)

            leaderboard.append({
                "algorithm": algo,
                "hyperparameters": best_params,
                "cv_score": cv_score,
                "metrics": metrics,
                "primary_score": primary_metric,
                "artifact_path": artifact_path,
                "tracking_uri": tracking_uri,
                "shap_summary": shap_dict,
                "model_obj": model
            })

        # Step 7: Select Best Model
        leaderboard.sort(key=lambda item: item["primary_score"], reverse=True)
        best_model_entry = leaderboard[0]

        # Step 8: Save Best Model Metadata
        best_model_path = os.path.join(ml_config.artifact_storage_path, f"{self.experiment_id}_best_model.joblib")
        joblib.dump(best_model_entry["model_obj"], best_model_path)

        # Step 9: Generate Full Evaluation Report
        report = {
            "experiment_id": self.experiment_id,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "dataset_type": dataset_type,
            "target_column": target_column,
            "task_type": task_type,
            "total_samples": len(df),
            "feature_count": X.shape[1],
            "algorithms_evaluated_count": len(leaderboard),
            "best_algorithm": best_model_entry["algorithm"],
            "best_score": best_model_entry["primary_score"],
            "best_model_path": best_model_path,
            "leaderboard": [
                {
                    "rank": idx + 1,
                    "algorithm": item["algorithm"],
                    "cv_score": item["cv_score"],
                    "metrics": item["metrics"],
                    "is_best": (idx == 0),
                    "artifact_path": item["artifact_path"]
                } for idx, item in enumerate(leaderboard)
            ],
            "shap_feature_importance": best_model_entry["shap_summary"]
        }

        return report
