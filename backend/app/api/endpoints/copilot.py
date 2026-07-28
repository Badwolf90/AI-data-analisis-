from typing import Optional, Dict, Any
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.core.dependencies import get_current_user
from app.models import User
from app.copilot_engine import AICopilotService

router = APIRouter()


class CopilotChatRequest(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None


@router.post("/chat")
async def chat_with_copilot(
    req: CopilotChatRequest,
    current_user: User = Depends(get_current_user)
):
    return AICopilotService.ask_copilot(req.message, req.context)
