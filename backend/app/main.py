import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.database import engine, Base
import app.models  # Register all SQLAlchemy models in Base.metadata
from app.core.logging import logger
from app.core.rate_limiter import RateLimiterMiddleware
from app.api.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("Initializing Database Tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database Initialization Complete.")
    yield
    logger.info("Shutting down Application...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Set CORS middleware
if settings.ALLOWED_HOSTS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(host) for host in settings.ALLOWED_HOSTS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Add Rate Limiting Middleware
app.add_middleware(RateLimiterMiddleware, requests_per_minute=settings.RATE_LIMIT_PER_MINUTE)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global unhandled error on path {request.url.path}: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error. Please contact system administrator."}
    )


import time
from sqlalchemy import text
from app.services.telemetry_service import TelemetryService


@app.middleware("http")
async def telemetry_latency_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration_ms = (time.time() - start_time) * 1000.0

    is_pred = "/predictions" in request.url.path
    TelemetryService.record_api_request(
        latency_ms=duration_ms,
        status_code=response.status_code,
        is_prediction=is_pred
    )
    return response


@app.get("/", tags=["Health Check"])
async def root():
    return {
        "status": "online",
        "app": settings.PROJECT_NAME,
        "docs": "/docs"
    }


@app.get("/health", tags=["Health Check"])
async def health_check():
    """Liveness Probe for Kubernetes / Docker / Nginx."""
    return {"status": "HEALTHY", "service": settings.PROJECT_NAME}


@app.get("/ready", tags=["Health Check"])
async def readiness_check():
    """Readiness Probe: Validates Database connection & System health."""
    db_ok = False
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
            db_ok = True
    except Exception as e:
        logger.error(f"Readiness check failed on DB: {e}")

    if not db_ok:
        return JSONResponse(status_code=503, content={"status": "UNREADY", "database": "DISCONNECTED"})

    return {"status": "READY", "database": "CONNECTED", "service": settings.PROJECT_NAME}


app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
