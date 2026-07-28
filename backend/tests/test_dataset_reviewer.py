import pytest
import pandas as pd
import numpy as np
from app.automl_engine.dataset_reviewer import DatasetReviewerEngine


def test_dataset_reviewer_engine():
    # Create sample DataFrame with intentional data quality issues
    df = pd.DataFrame({
        "id": [f"ID_{i}" for i in range(100)],  # Leakage / Unique ID
        "age": [25, 30, np.nan, 45, 120] + [35] * 95,  # Outlier (120) & Missing value
        "income": [50000] * 100,  # Constant column
        "feature_a": np.random.randn(100),
        "target": [0] * 90 + [1] * 10  # Severe Class Imbalance (90:10)
    })
    # Add duplicate row
    df = pd.concat([df, df.iloc[[0]]], ignore_index=True)

    result = DatasetReviewerEngine.audit_dataset(df, target_column="target")

    # Assertions
    assert "summary" in result
    assert "data_quality_score" in result["summary"]
    assert 0 <= result["summary"]["data_quality_score"] <= 100

    # Missing values
    assert result["missing_values"]["total_missing_cells"] == 1

    # Duplicates
    assert result["duplicates"]["duplicate_count"] == 1

    # Class Imbalance
    assert result["class_imbalance"]["is_imbalanced"] is True

    # Data Leakage
    assert result["data_leakage"]["has_leakage_risk"] is True
    assert len(result["data_leakage"]["constant_columns"]) > 0

    # Outliers
    assert result["outliers"]["total_outliers"] > 0

    # AI Senior Data Scientist Recommendation
    rec = result["ai_senior_ds_recommendation"]
    assert "executive_summary" in rec
    assert "critical_risks" in rec
    assert len(rec["critical_risks"]) > 0
