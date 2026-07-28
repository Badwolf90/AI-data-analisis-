import pytest
import pandas as pd
import numpy as np
import os
from app.ml_engine.pipeline import ProductionPipeline


def test_13_stage_production_pipeline(sample_classification_df, tmp_path):
    # 1. Instantiate Pipeline
    exp_id = "test_exp_13_stages"
    pipeline = ProductionPipeline(experiment_id=exp_id, version="v1.0.0")

    # Add extra raw data anomalies to test validation, cleaning & feature engineering
    df_raw = sample_classification_df.copy()
    df_raw["id_col"] = [f"ID_{i}" for i in range(len(df_raw))]
    df_raw["high_null_col"] = [None] * len(df_raw)  # > 50% missing

    # 2. Fit Pipeline (Runs Stages 1 through 11 & 13)
    result = pipeline.fit_pipeline(
        df_raw=df_raw,
        target_column="churn",
        algorithms=["RandomForest", "GradientBoosting"],
        n_trials=2
    )

    # Verify Stage 1 to 11 Output Metadata
    assert result["experiment_id"] == exp_id
    assert result["version"] == "v1.0.0"
    assert result["target_column"] == "churn"
    assert result["task_type"] == "CLASSIFICATION"
    assert result["best_algorithm"] in ["RandomForest", "GradientBoosting"]
    assert result["best_score"] >= 0.0
    assert os.path.exists(result["best_artifact_path"])
    assert len(result["leaderboard"]) == 2

    # 3. Stage 12: Production Inference (Prediction)
    new_sample = pd.DataFrame([{
        "age": 45,
        "income": 75000.0,
        "education": "Bachelors"
    }])

    pred_result = ProductionPipeline.predict(
        pipeline_bundle_path=result["best_artifact_path"],
        new_data=new_sample
    )

    assert "predictions" in pred_result
    assert len(pred_result["predictions"]) == 1
    assert "probabilities" in pred_result
    assert pred_result["pipeline_version"] == "v1.0.0"
