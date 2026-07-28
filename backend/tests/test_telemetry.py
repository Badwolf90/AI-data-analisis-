import pytest
from app.services.telemetry_service import TelemetryService


def test_telemetry_snapshot():
    # Record test request
    TelemetryService.record_api_request(latency_ms=22.5, status_code=200, is_prediction=True)

    metrics = TelemetryService.get_realtime_telemetry()

    assert "timestamp" in metrics
    assert metrics["status"] == "HEALTHY"

    # Verify all 10 subsystems
    assert "cpu" in metrics
    assert "usage_percentage" in metrics["cpu"]

    assert "ram" in metrics
    assert "used_mb" in metrics["ram"]

    assert "gpu" in metrics
    assert "device_name" in metrics["gpu"]

    assert "latency" in metrics
    assert "p50_ms" in metrics["latency"]
    assert "p95_ms" in metrics["latency"]

    assert "training_jobs" in metrics
    assert "active_jobs" in metrics["training_jobs"]

    assert "prediction" in metrics
    assert "total_predictions" in metrics["prediction"]

    assert "queue" in metrics
    assert "depth" in metrics["queue"]

    assert "storage" in metrics
    assert "usage_percentage" in metrics["storage"]

    assert "traffic" in metrics
    assert "total_requests" in metrics["traffic"]

    assert "workers" in metrics
    assert "active_workers" in metrics["workers"]
