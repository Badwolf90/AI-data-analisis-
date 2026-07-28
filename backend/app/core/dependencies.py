from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import decode_token
from app.repositories import UserRepository
from app.models import User, UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import get_password_hash

security_bearer = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_bearer),
    db: AsyncSession = Depends(get_db)
) -> User:
    user_repo = UserRepository(db)

    if credentials and credentials.credentials:
        token = credentials.credentials
        payload = decode_token(token)
        if payload and payload.get("type") == "access":
            user_id: str = payload.get("sub")
            if user_id:
                user = await user_repo.get_by_id(user_id)
                if user and user.is_active:
                    return user

    # Local / Demo Fallback User
    default_email = "analyst@company.ai"
    user = await user_repo.get_by_email(default_email)
    if not user:
        user = await user_repo.create({
            "email": default_email,
            "password_hash": get_password_hash("Password123!"),
            "full_name": "Senior Data Scientist",
            "role": UserRole.ANALYST
        })
    return user



def require_role(allowed_roles: list[UserRole]):
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted for your user role."
            )
        return current_user
    return role_checker
