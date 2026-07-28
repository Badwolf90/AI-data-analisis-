import pytest
import os
from app.saas import (
    SaaSNotificationService,
    SaaSAPIKeyService,
    SaaSBillingManager,
    SaaSEmailService,
    SaaSExportEngine,
    SaaSBackupRestoreEngine
)


def test_saas_notifications():
    notif = SaaSNotificationService.send_notification(
        user_id="user_123",
        title="Training Complete",
        message="Model XGBoost successfully trained.",
        notif_type="SUCCESS"
    )
    assert notif["user_id"] == "user_123"
    assert notif["type"] == "SUCCESS"


def test_saas_api_keys():
    key_info = SaaSAPIKeyService.generate_api_key(user_id="user_123", key_name="Production Core Key")
    assert key_info["prefix"].startswith("sk_live_")
    assert "full_api_key" in key_info
    assert len(key_info["hashed_key"]) == 64


def test_saas_billing_metered_usage():
    usage = SaaSBillingManager.check_usage_quota(
        plan_name="PRO",
        current_api_calls=25000,
        current_storage_mb=5000.0,
        current_training_hours=25.0
    )
    assert usage["plan_name"] == "PRO"
    assert usage["quota_status"] == "OK"
    assert usage["metrics"]["api_calls"]["pct"] == 50.0


def test_saas_export_engine():
    dummy_data = [
        {"id": 1, "model": "RandomForest", "accuracy": 0.95},
        {"id": 2, "model": "XGBoost", "accuracy": 0.94}
    ]
    csv_path = SaaSExportEngine.export_data(dummy_data, export_format="CSV", output_filename="test_export")
    assert os.path.exists(csv_path)

    json_path = SaaSExportEngine.export_data(dummy_data, export_format="JSON", output_filename="test_export")
    assert os.path.exists(json_path)


def test_saas_backup_and_restore(tmp_path):
    backup = SaaSBackupRestoreEngine.create_backup(backup_dir=str(tmp_path))
    assert os.path.exists(backup["archive_path"])

    restore = SaaSBackupRestoreEngine.restore_backup(backup["archive_path"])
    assert restore["restore_status"] == "SUCCESS"
