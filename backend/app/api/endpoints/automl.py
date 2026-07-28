from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models import User
from app.schemas import AutoMLStartRequest, ExperimentResponse
from app.services import AutoMLService
from app.repositories import ExperimentRepository

router = APIRouter()


def get_automl_service(db: AsyncSession = Depends(get_db)) -> AutoMLService:
    return AutoMLService(db)


def get_experiment_repository(db: AsyncSession = Depends(get_db)) -> ExperimentRepository:
    return ExperimentRepository(db)


@router.post("/start", response_model=ExperimentResponse, status_code=status.HTTP_200_OK)
async def start_automl(
    req: AutoMLStartRequest,
    current_user: User = Depends(get_current_user),
    service: AutoMLService = Depends(get_automl_service)
):
    """
    Triggers an automated Machine Learning pipeline for dataset cleaning, 
    encoding, scaling, model optimization (Optuna), evaluation, and SHAP explainability.
    """
    return await service.run_automl(req)


@router.get("/experiments/{experiment_id}", response_model=ExperimentResponse)
async def get_experiment_status(
    experiment_id: str,
    current_user: User = Depends(get_current_user),
    repo: ExperimentRepository = Depends(get_experiment_repository)
):
    """
    Retrieves the status, metrics, and trained model leaderboard for a given experiment ID.
    """
    return await repo.get_with_models(experiment_id)

