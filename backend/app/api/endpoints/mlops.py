from typing import Optional, Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
import pandas as pd
from pydantic import BaseModel

from app.core.dependencies import get_current_user
from app.models import User
from app.mlops import (
    DataDriftDetector,
    ModelDriftDetector,
    MLOpsModelRegistry,
    RetrainingManager
)

router = APIRouter()


class ModelRegisterRequest(BaseModel):
    model_name: str
    version: str
    artifact_path: str
    metrics: Dict[str, float]
    parameters: Dict[str, Any]
    git_commit_hash: Optional[str] = "unknown"


class ModelTransitionRequest(BaseModel):
    model_name: str
    version: str
    new_stage: str  # Staging, Production, Archived


class ModelDriftRequest(BaseModel):
    baseline_score: float
    current_score: float
    metric_name: Optional[str] = "accuracy"
    allowed_decay_pct: Optional[float] = 10.0


@router.post("/registry/register")
async def register_model(
    req: ModelRegisterRequest,
    current_user: User = Depends(get_current_user)
):
    """Registers a model version in MLOps Registry."""
    registry = MLOpsModelRegistry()
    return registry.register_model(
        model_name=req.model_name,
        version=req.version,
        artifact_path=req.artifact_path,
        metrics=req.metrics,
        parameters=req.parameters,
        git_commit_hash=req.git_commit_hash
    )


@router.post("/registry/transition")
async def transition_model_stage(
    req: ModelTransitionRequest,
    current_user: User = Depends(get_current_user)
):
    """Transitions a model version stage (Staging -> Production -> Archived)."""
    registry = MLOpsModelRegistry()
    try:
        return registry.transition_stage(
            model_name=req.model_name,
            version=req.version,
            new_stage=req.new_stage
        )
    except (ValueError, KeyError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/registry/{model_name}/production")
async def get_production_model(
    model_name: str,
    current_user: User = Depends(get_current_user)
):
    """Fetches the active Production model version from MLOps Registry."""
    registry = MLOpsModelRegistry()
    prod_model = registry.get_production_model(model_name)
    if not prod_model:
        raise HTTPException(status_code=404, detail=f"No Production model found for '{model_name}'.")
    return prod_model


@router.post("/drift/detect-data")
async def detect_data_drift(
    baseline_file: UploadFile = File(...),
    current_file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """
    Detects statistical Data Drift using Kolmogorov-Smirnov test and PSI
    between baseline training dataset and current inference dataset.
    """
    try:
        df_base = pd.read_csv(baseline_file.file) if baseline_file.filename.endswith(".csv") else pd.read_excel(baseline_file.file)
        df_curr = pd.read_csv(current_file.file) if current_file.filename.endswith(".csv") else pd.read_excel(current_file.file)

        return DataDriftDetector.detect_data_drift(df_baseline=df_base, df_current=df_curr)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Data drift evaluation error: {str(e)}")


@router.post("/drift/detect-model")
async def detect_model_drift(
    req: ModelDriftRequest,
    current_user: User = Depends(get_current_user)
):
    """Evaluates Model Drift / Performance Decay between baseline score and current evaluation score."""
    return ModelDriftDetector.detect_model_drift(
        baseline_metric=req.baseline_score,
        current_metric=req.current_score,
        metric_name=req.metric_name,
        allowed_decay_pct=req.allowed_decay_pct
    )


@router.post("/retrain/trigger")
async def trigger_retraining(
    experiment_id: str = Form(...),
    target_column: str = Form(...),
    model_name: Optional[str] = Form("production_classifier"),
    dataset_file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """Triggers automated model retraining pipeline and updates Model Registry."""
    try:
        df_raw = pd.read_csv(dataset_file.file) if dataset_file.filename.endswith(".csv") else pd.read_excel(dataset_file.file)

        return RetrainingManager.trigger_automated_retrain(
            experiment_id=experiment_id,
            df_raw=df_raw,
            target_column=target_column,
            model_name=model_name
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Retraining error: {str(e)}")
