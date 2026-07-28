import pytest
import pandas as pd
import numpy as np
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture(scope="session")
def sample_classification_df() -> pd.DataFrame:
    np.random.seed(42)
    n_samples = 100
    return pd.DataFrame({
        "age": np.random.randint(20, 60, size=n_samples),
        "income": np.random.uniform(30000, 100000, size=n_samples),
        "education": np.random.choice(["HighSchool", "Bachelors", "Masters"], size=n_samples),
        "churn": np.random.choice([0, 1], size=n_samples)
    })


@pytest.fixture(scope="module")
def api_client():
    with TestClient(app) as client:
        yield client
