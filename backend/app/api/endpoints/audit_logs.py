from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.dependencies import require_role
from app.models import User, UserRole
from app.schemas import AuditLogResponse
from app.repositories import AuditRepository

router = APIRouter()


@router.get("/", response_model=List[AuditLogResponse])
async def list_audit_logs(
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(require_role([UserRole.ADMIN]))
):
    repo = AuditRepository(db)
    return await repo.get_recent_logs(limit=limit)
