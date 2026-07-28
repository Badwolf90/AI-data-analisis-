from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.dependencies import get_current_user, require_role
from app.models import User, UserRole
from app.schemas import UserResponse
from app.repositories import UserRepository

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_my_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/", response_model=List[UserResponse])
async def list_all_users(
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(require_role([UserRole.ADMIN]))
):
    user_repo = UserRepository(db)
    return await user_repo.get_all()
