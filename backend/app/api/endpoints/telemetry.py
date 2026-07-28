import asyncio
import json
from typing import Dict, Any
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.core.dependencies import get_current_user
from app.models import User
from app.services.telemetry_service import TelemetryService

router = APIRouter()


@router.get("/metrics")
async def get_telemetry_metrics(
    current_user: User = Depends(get_current_user)
):
    """
    Grafana-style Realtime Infrastructure Telemetry Snapshot.
    Returns: CPU, RAM, GPU, Latency, Training, Prediction, Queue, Storage, Traffic, Workers.
    """
    return TelemetryService.get_realtime_telemetry()


@router.get("/stream")
async def stream_telemetry_metrics(
    current_user: User = Depends(get_current_user)
):
    """
    Server-Sent Events (SSE) Streaming Endpoint for Live Grafana Dashboard.
    Emits real-time telemetry JSON payload every 2 seconds.
    """
    async def event_generator():
        while True:
            metrics = TelemetryService.get_realtime_telemetry()
            yield f"data: {json.dumps(metrics)}\n\n"
            await asyncio.sleep(2.0)

    return StreamingResponse(event_generator(), media_type="text/event-stream")
