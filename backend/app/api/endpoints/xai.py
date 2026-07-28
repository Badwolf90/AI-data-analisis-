from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models import User
from app.schemas import LIMESampleRequest, LIMEResponse
from app.services import XAIService

router = APIRouter()


@router.get("/shap/{model_id}")
async def get_shap_explanation(
    model_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = XAIService(db)
    return await service.get_global_shap(model_id)


@router.post("/lime", response_model=LIMEResponse)
async def get_lime_explanation(
    req: LIMESampleRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = XAIService(db)
    return await service.get_lime_local_explanation(req)
