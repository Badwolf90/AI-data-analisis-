from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models import User
from app.schemas import ReportGenerateRequest, ReportResponse
from app.services import ReportService
from app.repositories import ReportRepository

router = APIRouter()


@router.post("/generate", response_model=ReportResponse, status_code=201)
async def generate_report(
    req: ReportGenerateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = ReportService(db)
    return await service.generate_report(current_user.id, req)


@router.get("/", response_model=List[ReportResponse])
async def list_reports(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    repo = ReportRepository(db)
    return await repo.get_by_user(current_user.id)
