import pytest
import pandas as pd
import numpy as np
import os
from app.mlops import (
    DataDriftDetector,
    ModelDriftDetector,
    MLOpsModelRegistry,
    RetrainingManager
)


def test_data_drift_detector():
    np.random.seed(42)

    # Baseline distribution (Mean = 0, Std = 1)
    df_baseline = pd.DataFrame({
        "feature_1": np.random.normal(0, 1, 200),
        "feature_2": np.random.normal(10, 2, 200)
    })

    # Current shifted distribution (Mean = 5, Std = 1 on feature_1)
    df_current = pd.DataFrame({
        "feature_1": np.random.normal(5, 1, 200),  # Drifting feature!
        "feature_2": np.random.normal(10, 2, 200)
    })

    drift_report = DataDriftDetector.detect_data_drift(df_baseline, df_current)

    assert "drift_detected" in drift_report
    assert "feature_1" in drift_report["drifted_features"]
    assert drift_report["feature_scores"]["feature_1"]["is_drifted"] is True


def test_model_drift_detector():
    # Baseline Accuracy = 0.94, Current Accuracy = 0.81 (13.8% decay > 10.0% allowed)
    report = ModelDriftDetector.detect_model_drift(
        baseline_metric=0.94,
        current_metric=0.81,
        allowed_decay_pct=10.0
    )

    assert report["model_drift_detected"] is True
    assert report["performance_decay_percentage"] > 10.0
    assert report["status"] == "ALERT_RETRAIN_NEEDED"


def test_mlops_model_registry(tmp_path):
    reg_path = tmp_path / "test_registry.json"
    registry = MLOpsModelRegistry(registry_file=str(reg_path))

    # 1. Register Version 1
    v1 = registry.register_model(
        model_name="churn_classifier",
        version="v1.0.0",
        artifact_path="/tmp/model_v1.joblib",
        metrics={"accuracy": 0.92},
        parameters={"n_estimators": 50}
    )

    assert v1["stage"] == "Staging"

    # 2. Transition Stage: Staging -> Production
    t1 = registry.transition_stage("churn_classifier", "v1.0.0", "Production")
    assert t1["stage"] == "Production"

    # Verify active Production model
    prod = registry.get_production_model("churn_classifier")
    assert prod["version"] == "v1.0.0"


def test_automated_retraining_manager(sample_classification_df, tmp_path):
    exp_id = "exp_retrain_test"
    target_col = "churn"

    retrain_report = RetrainingManager.trigger_automated_retrain(
        experiment_id=exp_id,
        df_raw=sample_classification_df,
        target_column=target_col,
        current_prod_score=0.50,
        model_name="test_prod_model"
    )

    assert retrain_report["retrain_status"] == "COMPLETED"
    assert retrain_report["promoted_to_production"] is True
    assert os.path.exists(retrain_report["artifact_path"])
