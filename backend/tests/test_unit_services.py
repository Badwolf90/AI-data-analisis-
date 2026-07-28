import pytest
from app.core.security import verify_password, get_password_hash, create_access_token, decode_token
from app.copilot_engine.interpreter import CopilotInterpreter
from app.copilot_engine.copilot_service import AICopilotService


def test_password_hashing():
    password = "MySecurePassword2026!"
    hashed = get_password_hash(password)
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("WrongPassword", hashed) is False


def test_jwt_token_encode_decode():
    subject = "user_12345"
    token = create_access_token(subject)
    assert isinstance(token, str)
    
    payload = decode_token(token)
    assert payload is not None
    assert payload["sub"] == "user_12345"
    assert payload["type"] == "access"


def test_copilot_metrics_explanation():
    metrics = {"accuracy": 0.95, "precision": 0.92, "recall": 0.94, "f1_score": 0.93, "roc_auc": 0.97}
    explanation = CopilotInterpreter.explain_metrics(metrics)
    assert "95.0%" in explanation
    assert "Akurasi" in explanation
    assert "F1-Score" in explanation


def test_copilot_service_ask():
    res = AICopilotService.ask_copilot("Bagaimana hasil F1 score model saya?")
    assert "response" in res
    assert "F1-Score" in res["response"]
    assert len(res["suggested_questions"]) > 0
