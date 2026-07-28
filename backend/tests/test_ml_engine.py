import pytest
import os
import pandas as pd
from app.ml_engine.data.loader import DataValidator
from app.ml_engine.preprocessing import DataCleaner, DataEncoder, DataScaler
from app.ml_engine.models import ModelFactory, ModelEvaluator
from app.ml_engine.tuning import OptunaHyperparameterTuner
from app.ml_engine.xai import SHAPExplainer
from app.automl_engine import AutoMLEngine, DatasetTypeDetector, TargetDetector


def test_data_validator(sample_classification_df):
    val_res = DataValidator.validate(sample_classification_df, target_column="churn")
    assert val_res["is_valid"] is True
    assert val_res["total_rows"] == 100
    assert val_res["target_column"] == "churn"


def test_data_preprocessor(sample_classification_df):
    cleaner = DataCleaner()
    df_clean = cleaner.fit_transform(sample_classification_df)
    
    encoder = DataEncoder()
    df_encoded = encoder.fit_transform(df_clean)
    assert df_encoded["education"].dtype != object

    scaler = DataScaler(method="standard")
    df_scaled = scaler.fit_transform(df_encoded)
    assert df_scaled is not None


def test_model_factory_supported_algorithms():
    algos = ModelFactory.get_supported_algorithms()
    assert len(algos) >= 8
    assert "RandomForest" in algos
    assert "GradientBoosting" in algos


def test_model_training_and_evaluation(sample_classification_df):
    X = sample_classification_df.drop(columns=["churn", "education"])
    y = sample_classification_df["churn"]

    model = ModelFactory.create_model("RandomForest", task_type="CLASSIFICATION", random_state=42)
    model.fit(X, y)

    metrics = ModelEvaluator.evaluate(model, X, y, task_type="CLASSIFICATION")
    assert "accuracy" in metrics
    assert "f1_score" in metrics
    assert metrics["accuracy"] >= 0.5


def test_optuna_tuner(sample_classification_df):
    X = sample_classification_df.drop(columns=["churn", "education"])
    y = sample_classification_df["churn"]

    tuner = OptunaHyperparameterTuner(task_type="CLASSIFICATION", n_trials=2)
    best_params, best_score = tuner.tune_algorithm("RandomForest", X, y)
    assert isinstance(best_params, dict)
    assert best_score >= 0.0


def test_shap_explainer(sample_classification_df):
    X = sample_classification_df.drop(columns=["churn", "education"])
    y = sample_classification_df["churn"]

    model = ModelFactory.create_model("RandomForest", task_type="CLASSIFICATION", random_state=42)
    model.fit(X, y)

    shap_dict = SHAPExplainer.explain_global(model, X.head(10))
    assert isinstance(shap_dict, dict)


def test_full_automl_engine(sample_classification_df, tmp_path):
    target = TargetDetector.auto_detect_target(sample_classification_df)
    assert target == "churn"

    ds_type = DatasetTypeDetector.detect(sample_classification_df, target)
    assert ds_type == "TABULAR_CLASSIFICATION"

    engine = AutoMLEngine(experiment_id="test_exp_001")
    report = engine.run_full_automl(sample_classification_df, target_column="churn", n_trials_per_model=2)
    
    assert report["experiment_id"] == "test_exp_001"
    assert report["best_algorithm"] is not None
    assert len(report["leaderboard"]) > 0
