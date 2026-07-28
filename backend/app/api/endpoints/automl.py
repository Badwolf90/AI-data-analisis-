from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models import User
from app.schemas import AutoMLStartRequest, ExperimentResponse
from app.services import AutoMLService
from app.repositories import ExperimentRepository

router = APIRouter()


@router.post("/start", response_model=ExperimentResponse)
async def start_automl(
    req: AutoMLStartRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = AutoMLService(db)
    return await service.run_automl(req)


@router.get("/experiments/{experiment_id}", response_model=ExperimentResponse)
async def get_experiment_status(
    experiment_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    repo = ExperimentRepository(db)
    return await repo.get_with_models(experiment_id)
