import pytest
import pandas as pd
import numpy as np
from app.copilot_engine.copilot_service import AIDataScientistEngine


def test_ai_data_scientist_queries(sample_classification_df, tmp_path):
    # Save temporary CSV file to test reading actual user dataset
    csv_file = tmp_path / "user_sample.csv"
    sample_df = sample_classification_df.copy()
    sample_df.to_csv(csv_file, index=False)

    context = {
        "target_column": "churn",
        "leaderboard": [
            {"algorithm": "RandomForest", "primary_score": 0.94},
            {"algorithm": "GradientBoosting", "primary_score": 0.91}
        ],
        "top_features": {"income": 0.42, "age": 0.31}
    }

    # Query 1: Kenapa Accuracy turun?
    res_acc = AIDataScientistEngine.ask_ai_data_scientist(
        prompt="Kenapa Accuracy turun?",
        context=context,
        dataset_path=str(csv_file)
    )
    assert "Accuracy Turun" in res_acc["response"]
    assert res_acc["dataset_insights_used"]["total_rows"] == 100

    # Query 2: Kenapa Recall kecil?
    res_rec = AIDataScientistEngine.ask_ai_data_scientist(
        prompt="Kenapa Recall kecil?",
        context=context,
        dataset_path=str(csv_file)
    )
    assert "Recall" in res_rec["response"]

    # Query 3: Bagaimana memperbaiki dataset?
    res_fix = AIDataScientistEngine.ask_ai_data_scientist(
        prompt="Bagaimana memperbaiki dataset?",
        context=context,
        dataset_path=str(csv_file)
    )
    assert "Pembersihan Dataset" in res_fix["response"]

    # Query 4: Model terbaik apa?
    res_best = AIDataScientistEngine.ask_ai_data_scientist(
        prompt="Model terbaik apa?",
        context=context,
        dataset_path=str(csv_file)
    )
    assert "RandomForest" in res_best["response"]

    # Query 5: Kenapa Random Forest menang?
    res_rf = AIDataScientistEngine.ask_ai_data_scientist(
        prompt="Kenapa Random Forest menang?",
        context=context,
        dataset_path=str(csv_file)
    )
    assert "Random Forest Menang" in res_rf["response"]

    # Query 6: Apa arti SHAP?
    res_shap = AIDataScientistEngine.ask_ai_data_scientist(
        prompt="Apa arti SHAP?",
        context=context,
        dataset_path=str(csv_file)
    )
    assert "SHAP" in res_shap["response"]
