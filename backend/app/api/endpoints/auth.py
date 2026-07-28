from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas import RegisterRequest, LoginRequest, TokenResponse, UserResponse
from app.services import AuthService

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(req: RegisterRequest, request: Request, db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)
    client_ip = request.client.host if request.client else "127.0.0.1"
    user = await auth_service.register(req, ip_address=client_ip)
    return user


@router.post("/login", response_model=TokenResponse)
async def login(req: LoginRequest, request: Request, db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)
    client_ip = request.client.host if request.client else "127.0.0.1"
    tokens = await auth_service.authenticate(req, ip_address=client_ip)
    return tokens


from app.schemas import RefreshTokenRequest


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(req: RefreshTokenRequest, request: Request, db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)
    client_ip = request.client.host if request.client else "127.0.0.1"
    return await auth_service.refresh_token(req.refresh_token, ip_address=client_ip)

