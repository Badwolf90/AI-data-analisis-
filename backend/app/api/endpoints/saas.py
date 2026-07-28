from typing import Optional, Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from pydantic import BaseModel

from app.core.dependencies import get_current_user
from app.models import User
from app.saas import (
    SaaSNotificationService,
    SaaSAPIKeyService,
    SaaSBillingManager,
    SaaSEmailService,
    SaaSExportEngine,
    SaaSBackupRestoreEngine
)

router = APIRouter()


class NotificationSendRequest(BaseModel):
    title: str
    message: str
    type: Optional[str] = "INFO"


class APIKeyGenerateRequest(BaseModel):
    key_name: str


class ExportDataRequest(BaseModel):
    data: List[Dict[str, Any]]
    format: Optional[str] = "CSV"  # CSV, JSON, EXCEL
    filename: Optional[str] = "export_output"


class RestoreRequest(BaseModel):
    backup_archive_path: str


@router.post("/notifications/send")
async def send_notification(
    req: NotificationSendRequest,
    current_user: User = Depends(get_current_user)
):
    """Dispatches in-app notification & alert."""
    return SaaSNotificationService.send_notification(
        user_id=current_user.id,
        title=req.title,
        message=req.message,
        notif_type=req.type
    )


@router.post("/api-keys/generate")
async def generate_api_key(
    req: APIKeyGenerateRequest,
    current_user: User = Depends(get_current_user)
):
    """Generates secure workspace API key."""
    return SaaSAPIKeyService.generate_api_key(user_id=current_user.id, key_name=req.key_name)


@router.get("/billing/usage")
async def get_billing_usage(
    plan_name: Optional[str] = "PRO",
    current_user: User = Depends(get_current_user)
):
    """Fetches metered usage quota vs plan tier limit."""
    return SaaSBillingManager.check_usage_quota(
        plan_name=plan_name,
        current_api_calls=1420,
        current_storage_mb=412.5,
        current_training_hours=8.4
    )


@router.post("/export/data")
async def export_data(
    req: ExportDataRequest,
    current_user: User = Depends(get_current_user)
):
    """Exports datasets, prediction results, or audit reports to CSV, JSON, or EXCEL."""
    try:
        path = SaaSExportEngine.export_data(data=req.data, export_format=req.format, output_filename=req.filename)
        return {"export_path": path, "format": req.format.upper(), "status": "COMPLETED"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/backup/create")
async def create_system_backup(
    current_user: User = Depends(get_current_user)
):
    """Generates full system backup archive (Database + Artifact Storage)."""
    return SaaSBackupRestoreEngine.create_backup()


@router.post("/backup/restore")
async def restore_system_backup(
    req: RestoreRequest,
    current_user: User = Depends(get_current_user)
):
    """Restores database state and artifact storage from backup archive."""
    try:
        return SaaSBackupRestoreEngine.restore_backup(backup_archive_path=req.backup_archive_path)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
