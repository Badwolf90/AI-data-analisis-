import pytest
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from app.ml_engine.xai.xai_suite import XAISuiteEngine


def test_xai_suite_engine(sample_classification_df):
    X = sample_classification_df.drop(columns=["churn", "education"])
    y = sample_classification_df["churn"]

    model = RandomForestClassifier(n_estimators=10, random_state=42)
    model.fit(X, y)

    sample_row = X.iloc[0]

    report = XAISuiteEngine.generate_full_xai_report(
        model=model,
        X_train=X,
        sample_row=sample_row,
        target_name="churn",
        task_type="CLASSIFICATION"
    )

    # 1. Feature Importance
    assert "feature_importance" in report
    assert len(report["feature_importance"]) > 0

    # 2. SHAP Analysis
    assert "shap_analysis" in report
    assert "waterfall_plot" in report["shap_analysis"]
    assert "summary_plot" in report["shap_analysis"]

    # 3. LIME Analysis
    assert "lime_analysis" in report
    assert len(report["lime_analysis"]["local_explanations"]) > 0

    # 4. Counterfactual Analysis
    assert "counterfactual_analysis" in report
    assert "original_prediction" in report["counterfactual_analysis"]
    assert "required_feature_perturbations" in report["counterfactual_analysis"]

    # 5. Dual-Language AI Explanations
    assert "bilingual_ai_explanations" in report
    bilingual = report["bilingual_ai_explanations"]
    assert "indonesian_id" in bilingual
    assert "english_en" in bilingual
    assert "Bahasa Indonesia" in bilingual["indonesian_id"]
    assert "English" in bilingual["english_en"]
