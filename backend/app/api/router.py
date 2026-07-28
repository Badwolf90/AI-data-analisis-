from fastapi import APIRouter
from app.api.endpoints import (
    auth, users, projects, datasets, automl, xai, predictions, reports, audit_logs, copilot, workspaces, mlops
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(workspaces.router, prefix="/workspaces", tags=["Workspaces & Teams"])
api_router.include_router(projects.router, prefix="/projects", tags=["Projects"])
api_router.include_router(datasets.router, prefix="/datasets", tags=["Datasets"])
api_router.include_router(automl.router, prefix="/automl", tags=["AutoML Engine"])
api_router.include_router(xai.router, prefix="/xai", tags=["Explainable AI"])
api_router.include_router(predictions.router, prefix="/predictions", tags=["Predictions & Inference"])
api_router.include_router(reports.router, prefix="/reports", tags=["Report Generation"])
api_router.include_router(audit_logs.router, prefix="/audit-logs", tags=["Audit Logs"])
api_router.include_router(copilot.router, prefix="/copilot", tags=["AI Copilot Chat"])
api_router.include_router(mlops.router, prefix="/mlops", tags=["MLOps & Drift Monitoring"])


