from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models import User
from app.schemas import PredictRequest, PredictResponse
from app.services import PredictionService

router = APIRouter()


@router.post("/predict", response_model=PredictResponse)
async def predict(
    req: PredictRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = PredictionService(db)
    return await service.predict(req)
