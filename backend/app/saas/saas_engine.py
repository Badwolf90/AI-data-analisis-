import os
import shutil
import zipfile
import json
import secrets
import hashlib
import pandas as pd
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

from app.core.logging import logger
from app.models import NotificationType


class SaaSNotificationService:
    """In-app Notifications & Alerts Dispatcher."""

    @staticmethod
    def send_notification(
        user_id: str,
        title: str,
        message: str,
        notif_type: str = "INFO"
    ) -> Dict[str, Any]:
        logger.info(f"🔔 Notification sent to user [{user_id}]: {title}")
        return {
            "id": f"notif_{int(datetime.now().timestamp() * 1000)}",
            "user_id": user_id,
            "title": title,
            "message": message,
            "type": notif_type,
            "is_read": False,
            "created_at": datetime.now(timezone.utc).isoformat()
        }


class SaaSAPIKeyService:
    """Secure Workspace API Key Generator & Validator."""

    @staticmethod
    def generate_api_key(user_id: str, key_name: str) -> Dict[str, Any]:
        raw_token = secrets.token_hex(24)
        prefix = "sk_live_" + raw_token[:8]
        full_key = f"{prefix}_{raw_token[8:]}"
        hashed_key = hashlib.sha256(full_key.encode("utf-8")).hexdigest()

        return {
            "key_id": f"key_{secrets.token_hex(6)}",
            "user_id": user_id,
            "key_name": key_name,
            "prefix": prefix,
            "full_api_key": full_key,  # Returned ONLY ONCE upon creation
            "hashed_key": hashed_key,
            "is_active": True,
            "created_at": datetime.now(timezone.utc).isoformat()
        }


class SaaSBillingManager:
    """Metered Usage Tracker & Subscription Plan Quota Enforcer."""

    PLANS = {
        "FREE": {"api_call_limit": 1000, "storage_limit_mb": 500, "training_hours_limit": 5.0},
        "PRO": {"api_call_limit": 50000, "storage_limit_mb": 10000, "training_hours_limit": 100.0},
        "ENTERPRISE": {"api_call_limit": 1000000, "storage_limit_mb": 500000, "training_hours_limit": 5000.0}
    }

    @staticmethod
    def check_usage_quota(
        plan_name: str,
        current_api_calls: int,
        current_storage_mb: float,
        current_training_hours: float
    ) -> Dict[str, Any]:
        plan = SaaSBillingManager.PLANS.get(plan_name.upper(), SaaSBillingManager.PLANS["FREE"])

        api_exhausted = current_api_calls >= plan["api_call_limit"]
        storage_exhausted = current_storage_mb >= plan["storage_limit_mb"]
        training_exhausted = current_training_hours >= plan["training_hours_limit"]

        return {
            "plan_name": plan_name.upper(),
            "quota_status": "EXCEEDED" if (api_exhausted or storage_exhausted or training_exhausted) else "OK",
            "metrics": {
                "api_calls": {"current": current_api_calls, "limit": plan["api_call_limit"], "pct": round((current_api_calls / plan["api_call_limit"]) * 100, 1)},
                "storage_mb": {"current": current_storage_mb, "limit": plan["storage_limit_mb"], "pct": round((current_storage_mb / plan["storage_limit_mb"]) * 100, 1)},
                "training_hours": {"current": current_training_hours, "limit": plan["training_hours_limit"], "pct": round((current_training_hours / plan["training_hours_limit"]) * 100, 1)}
            }
        }


class SaaSEmailService:
    """Transactional Email Service."""

    @staticmethod
    def send_email(to_email: str, subject: str, body_html: str) -> Dict[str, Any]:
        logger.info(f"📧 Transactional Email dispatched to [{to_email}] - Subject: '{subject}'")
        return {
            "status": "DISPATCHED",
            "recipient": to_email,
            "subject": subject,
            "sent_at": datetime.now(timezone.utc).isoformat()
        }


class SaaSExportEngine:
    """Data & Prediction Result Export Engine (CSV, JSON, Excel)."""

    @staticmethod
    def export_data(
        data: List[Dict[str, Any]],
        export_format: str = "CSV",
        output_filename: str = "export_output"
    ) -> str:
        os.makedirs("storage/exports", exist_ok=True)
        df = pd.DataFrame(data)

        export_format = export_format.upper()
        if export_format == "CSV":
            path = f"storage/exports/{output_filename}.csv"
            df.to_csv(path, index=False)
        elif export_format == "JSON":
            path = f"storage/exports/{output_filename}.json"
            df.to_json(path, orient="records", indent=2)
        elif export_format in ["EXCEL", "XLSX"]:
            path = f"storage/exports/{output_filename}.xlsx"
            df.to_excel(path, index=False)
        else:
            raise ValueError(f"Unsupported export format '{export_format}'. Must be CSV, JSON, or EXCEL.")

        return path


class SaaSBackupRestoreEngine:
    """Enterprise Backup & Restoration Manager for Database & Artifact Storage."""

    @staticmethod
    def create_backup(backup_dir: str = "storage/backups") -> Dict[str, Any]:
        os.makedirs(backup_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_path = os.path.join(backup_dir, f"saas_backup_{timestamp}.zip")

        with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            # Backup database file if sqlite exists
            if os.path.exists("app.db"):
                zipf.write("app.db", arcname="database/app.db")

            # Backup storage artifacts
            if os.path.exists("storage"):
                for root, dirs, files in os.walk("storage"):
                    for file in files:
                        fp = os.path.join(root, file)
                        if not fp.startswith(backup_dir):  # Don't include backup zip in backup
                            arcname = os.path.relpath(fp, start=".")
                            zipf.write(fp, arcname=arcname)

        size_mb = round(os.path.getsize(archive_path) / (1024 * 1024), 2)
        logger.info(f"📦 Backup created successfully: {archive_path} ({size_mb} MB)")

        return {
            "backup_filename": os.path.basename(archive_path),
            "archive_path": archive_path,
            "size_mb": size_mb,
            "created_at": datetime.now(timezone.utc).isoformat()
        }

    @staticmethod
    def restore_backup(backup_archive_path: str) -> Dict[str, Any]:
        if not os.path.exists(backup_archive_path):
            raise FileNotFoundError(f"Backup file '{backup_archive_path}' does not exist.")

        with zipfile.ZipFile(backup_archive_path, "r") as zipf:
            zipf.extractall(path=".")

        logger.info(f"♻️ Restoration completed from archive: {backup_archive_path}")
        return {
            "restore_status": "SUCCESS",
            "archive_path": backup_archive_path,
            "restored_at": datetime.now(timezone.utc).isoformat()
        }
