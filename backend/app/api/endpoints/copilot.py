from typing import Optional, Dict, Any
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.core.dependencies import get_current_user
from app.models import User
from app.copilot_engine import AIDataScientistEngine

router = APIRouter()


class CopilotChatRequest(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None
    dataset_path: Optional[str] = None


@router.post("/chat")
async def chat_with_copilot(
    req: CopilotChatRequest,
    current_user: User = Depends(get_current_user)
):
    """
    AI Senior Data Scientist Endpoint.
    Reads user dataset statistics & AutoML experiment context to answer:
    - Kenapa Accuracy turun?
    - Kenapa Recall kecil?
    - Bagaimana memperbaiki dataset?
    - Model terbaik apa?
    - Kenapa Random Forest menang?
    - Apa arti SHAP?
    """
    return AIDataScientistEngine.ask_ai_data_scientist(
        prompt=req.message,
        context=req.context,
        dataset_path=req.dataset_path
    )

