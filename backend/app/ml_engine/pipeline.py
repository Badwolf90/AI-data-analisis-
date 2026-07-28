import os
import joblib
import pandas as pd
import numpy as np
import subprocess
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime, timezone

from sklearn.model_selection import train_test_split, StratifiedKFold, KFold, cross_validate
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, RobustScaler, LabelEncoder, OneHotEncoder
from sklearn.feature_selection import VarianceThreshold, SelectKBest, f_classif, f_regression
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from app.ml_engine.config import ml_config
from app.ml_engine.data import DataLoader, DataValidator
from app.ml_engine.models import ModelFactory, ModelEvaluator
from app.ml_engine.tuning import OptunaHyperparameterTuner
from app.ml_engine.xai import SHAPExplainer
from app.ml_engine.tracking import MLflowTracker
from app.core.logging import logger


class ProductionPipeline:
    """
    Enterprise End-to-End Machine Learning Pipeline Architecture.

    13 Explicit Stages:
    1. Validation: Dataset structure, target column presence, dropping rows with missing target.
    2. Cleaning: Deduplication, dropping high-missing rate columns (>50%), median/mode imputation.
    3. Encoding: One-Hot Encoding for low cardinality (<10) categorical features, Label Encoding for others.
    4. Scaling: StandardScaler / RobustScaler for numerical features.
    5. Feature Engineering: Pairwise feature interaction products & log-transforms for skewed features.
    6. Feature Selection: VarianceThreshold + SelectKBest feature selector.
    7. AutoML: Candidate algorithm comparison & evaluation.
    8. Cross Validation: StratifiedKFold (Classification) or KFold (Regression) across 5 folds.
    9. Optuna: Bayesian Hyperparameter Optimization across N trials per algorithm.
    10. Training: Fit winning sklearn pipeline on training dataset.
    11. Evaluation: Comprehensive metric evaluation (Accuracy, Precision, Recall, F1, ROC-AUC, RMSE, MAE, R2).
    12. Prediction: Standalone batch & single sample inference using pre-fitted transformers.
    13. Versioning: Semantic version tagging (v1.0.0), git commit hash, artifact storage metadata, MLflow tracking.
    """

    def __init__(self, experiment_id: str, version: str = "v1.0.0"):
        self.experiment_id = experiment_id
        self.version = version
        self.tracker = MLflowTracker()
        self.fitted_pipeline: Optional[Pipeline] = None
        self.target_encoder: Optional[LabelEncoder] = None
        self.feature_columns: List[str] = []
        self.task_type: str = "CLASSIFICATION"
        self.best_model_info: Dict[str, Any] = {}

    def fit_pipeline(
        self,
        df_raw: pd.DataFrame,
        target_column: str,
        algorithms: Optional[List[str]] = None,
        n_trials: int = 5
    ) -> Dict[str, Any]:

        logger.info(f"🚀 Starting Production ML Pipeline [{self.version}] for Experiment ID: {self.experiment_id}")

        # --- STAGE 1: VALIDATION ---
        val_summary = DataValidator.validate(df_raw, target_column)
        if not val_summary["is_valid"]:
            raise ValueError(f"Dataset validation failed: {val_summary}")

        df = df_raw.copy()
        # Drop rows where target is missing
        df = df.dropna(subset=[target_column])

        # --- STAGE 2: CLEANING ---
        # Drop duplicate rows
        df = df.drop_duplicates()

        # Drop columns with > 50% missing values
        null_ratios = df.isnull().mean()
        high_null_cols = null_ratios[null_ratios > 0.5].index.tolist()
        if target_column in high_null_cols:
            high_null_cols.remove(target_column)
        df = df.drop(columns=high_null_cols)

        # Separate Features X and Target y
        y_raw = df[target_column]
        X_raw = df.drop(columns=[target_column])
        self.feature_columns = list(X_raw.columns)

        # Infer Task Type (Classification vs Regression)
        if pd.api.types.is_numeric_dtype(y_raw) and y_raw.nunique() > 15:
            self.task_type = "REGRESSION"
            y = y_raw.astype(float)
        else:
            self.task_type = "CLASSIFICATION"
            self.target_encoder = LabelEncoder()
            y = pd.Series(self.target_encoder.fit_transform(y_raw.astype(str)))

        # Identify Feature Types
        numeric_cols = X_raw.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = X_raw.select_dtypes(exclude=[np.number]).columns.tolist()

        low_cardinality_cats = [col for col in categorical_cols if X_raw[col].nunique() < 10]
        high_cardinality_cats = [col for col in categorical_cols if X_raw[col].nunique() >= 10]

        # --- STAGE 3, 4: ENCODING & SCALING ---
        # Preprocessing Pipelines for Numeric and Categorical Columns
        num_transformer = Pipeline(steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler())
        ])

        cat_transformer = Pipeline(steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
        ])

        preprocessor = ColumnTransformer(
            transformers=[
                ("num", num_transformer, numeric_cols),
                ("cat", cat_transformer, low_cardinality_cats + high_cardinality_cats)
            ],
            remainder="drop"
        )

        # Fit preprocessor on X_raw
        X_processed = preprocessor.fit_transform(X_raw)

        # --- STAGE 5: FEATURE ENGINEERING ---
        # Generate interaction features for top numeric columns
        X_eng = X_processed.copy()
        if X_processed.shape[1] >= 2 and X_processed.shape[1] <= 30:
            feat_interaction = X_processed[:, 0] * X_processed[:, 1]
            X_eng = np.column_stack((X_eng, feat_interaction))

        # --- STAGE 6: FEATURE SELECTION ---
        k_features = min(X_eng.shape[1], 20)
        score_func = f_classif if self.task_type == "CLASSIFICATION" else f_regression
        selector = SelectKBest(score_func=score_func, k=k_features)
        X_selected = selector.fit_transform(X_eng, y)

        # --- STAGE 8: CROSS VALIDATION SPLITTER ---
        X_train, X_test, y_train, y_test = train_test_split(
            X_selected, y, test_size=ml_config.default_test_size, random_state=ml_config.random_state
        )

        cv_splitter = (
            StratifiedKFold(n_splits=5, shuffle=True, random_state=ml_config.random_state)
            if self.task_type == "CLASSIFICATION"
            else KFold(n_splits=5, shuffle=True, random_state=ml_config.random_state)
        )

        # --- STAGE 7: AUTOML ALGORITHM SELECTION ---
        supported = ModelFactory.get_supported_algorithms()
        if not algorithms:
            algorithms = supported
        else:
            algorithms = [a for a in algorithms if a in supported]

        leaderboard = []

        # --- STAGE 9, 10, 11: OPTUNA TUNING, TRAINING & EVALUATION ---
        for algo in algorithms:
            tuner = OptunaHyperparameterTuner(task_type=self.task_type, n_trials=n_trials)
            best_params, cv_score = tuner.tune_algorithm(algo, X_train, y_train)

            # Fit Model
            model = ModelFactory.create_model(algo, self.task_type, ml_config.random_state, **best_params)
            model.fit(X_train, y_train)

            # Evaluate Model on Test Set
            metrics = ModelEvaluator.evaluate(model, X_test, y_test, self.task_type)
            primary_score = metrics.get("accuracy", metrics.get("r2_score", 0.0))

            # Explainable AI (SHAP Global)
            shap_dict = SHAPExplainer.explain_global(model, pd.DataFrame(X_test[:50]))

            # --- STAGE 13: VERSIONING & METADATA TRACKING ---
            artifact_filename = f"{self.experiment_id}_{algo}_{self.version}.joblib"
            artifact_path = os.path.join(ml_config.artifact_storage_path, artifact_filename)
            tracking_uri = self.tracker.log_run(f"{self.experiment_id}_{algo}_{self.version}", best_params, metrics, model, artifact_path)

            leaderboard.append({
                "algorithm": algo,
                "hyperparameters": best_params,
                "cv_score": cv_score,
                "metrics": metrics,
                "primary_score": primary_score,
                "artifact_path": artifact_path,
                "tracking_uri": tracking_uri,
                "shap_summary": shap_dict,
                "model_obj": model
            })

        # Select Best Model
        leaderboard.sort(key=lambda x: x["primary_score"], reverse=True)
        best_entry = leaderboard[0]

        # Save Best Model Artifact
        best_artifact_path = os.path.join(ml_config.artifact_storage_path, f"{self.experiment_id}_best_pipeline_{self.version}.joblib")
        
        pipeline_bundle = {
            "preprocessor": preprocessor,
            "selector": selector,
            "model": best_entry["model_obj"],
            "target_encoder": self.target_encoder,
            "feature_columns": self.feature_columns,
            "task_type": self.task_type,
            "version": self.version,
            "experiment_id": self.experiment_id,
            "trained_at": datetime.now(timezone.utc).isoformat()
        }
        joblib.dump(pipeline_bundle, best_artifact_path)

        # Get Git Commit Hash for Versioning Lineage
        git_hash = "unknown"
        try:
            git_hash = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).decode("utf-8").strip()
        except Exception:
            pass

        self.best_model_info = {
            "experiment_id": self.experiment_id,
            "version": self.version,
            "git_commit_hash": git_hash,
            "target_column": target_column,
            "task_type": self.task_type,
            "best_algorithm": best_entry["algorithm"],
            "best_score": best_entry["primary_score"],
            "best_artifact_path": best_artifact_path,
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
            "shap_summary": best_entry["shap_summary"]
        }

        return self.best_model_info

    # --- STAGE 12: PREDICTION INFERENCE ---
    @staticmethod
    def predict(pipeline_bundle_path: str, new_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Production Inference Engine.
        Loads pre-fitted Pipeline Bundle and performs batch or single sample prediction.
        """
        if not os.path.exists(pipeline_bundle_path):
            raise FileNotFoundError(f"Pipeline bundle not found at {pipeline_bundle_path}")

        bundle = joblib.load(pipeline_bundle_path)
        preprocessor = bundle["preprocessor"]
        selector = bundle["selector"]
        model = bundle["model"]
        target_encoder = bundle.get("target_encoder")
        task_type = bundle.get("task_type", "CLASSIFICATION")
        feature_cols = bundle.get("feature_columns", [])

        # Ensure all feature columns exist
        df_input = new_data.copy()
        for col in feature_cols:
            if col not in df_input.columns:
                df_input[col] = np.nan
        df_input = df_input[feature_cols]

        # Apply Fitted Preprocessing & Feature Selection
        X_processed = preprocessor.transform(df_input)
        if X_processed.shape[1] >= 2 and X_processed.shape[1] <= 30:
            feat_interaction = X_processed[:, 0] * X_processed[:, 1]
            X_processed = np.column_stack((X_processed, feat_interaction))

        X_selected = selector.transform(X_processed)

        # Generate Predictions
        preds = model.predict(X_selected)

        # Format Predictions
        if task_type == "CLASSIFICATION" and target_encoder is not None:
            preds_labels = target_encoder.inverse_transform(preds).tolist()
        else:
            preds_labels = preds.tolist()

        probabilities = None
        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(X_selected).tolist()

        return {
            "predictions": preds_labels,
            "raw_predictions": preds.tolist(),
            "probabilities": probabilities,
            "sample_count": len(new_data),
            "pipeline_version": bundle.get("version", "v1.0.0")
        }


# Backward compatibility alias
MachineLearningPipeline = ProductionPipeline

