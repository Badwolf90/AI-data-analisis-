from typing import Optional
from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models import User
from app.schemas import DatasetResponse, PreprocessConfigRequest
from app.services import DatasetService

router = APIRouter()


@router.post("/upload", response_model=DatasetResponse, status_code=201)
async def upload_dataset(
    file: UploadFile = File(...),
    project_id: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = DatasetService(db)
    return await service.upload_dataset(current_user.id, file, project_id)


@router.get("/{dataset_id}", response_model=DatasetResponse)
async def get_dataset(
    dataset_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = DatasetService(db)
    return await service.get_dataset(dataset_id)


from app.schemas import DatasetResponse, PreprocessConfigRequest, DatasetReviewRequest, DatasetReviewResponse


@router.post("/{dataset_id}/review", response_model=DatasetReviewResponse)
async def review_dataset(
    dataset_id: str,
    req: DatasetReviewRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Performs comprehensive Dataset Reviewer audit acting as a Senior Data Scientist:
    - Missing Values
    - Duplicates
    - Data Leakage
    - Outliers
    - Imbalance
    - Correlation
    - Target Validation
    - Data Quality Score (0-100)
    - AI Senior Data Scientist Recommendation
    """
    service = DatasetService(db)
    return await service.review_dataset(dataset_id, target_column=req.target_column)

