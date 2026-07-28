import os
from pydantic import BaseModel, Field

class MLEngineConfig(BaseModel):
    artifact_storage_path: str = Field(default="./models_registry")
    mlflow_tracking_uri: str = Field(default="sqlite:///mlflow.db")
    mlflow_experiment_name: str = Field(default="AI_Data_Analysis_Platform")
    random_state: int = Field(default=42)
    default_test_size: float = Field(default=0.2)
    cv_folds: int = Field(default=5)

ml_config = MLEngineConfig()
os.makedirs(ml_config.artifact_storage_path, exist_ok=True)
