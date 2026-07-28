from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, Field
from app.models import UserRole, ProblemType, ExperimentStatus

# --- Auth Schemas ---
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: str
    role: Optional[UserRole] = UserRole.ANALYST


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    refresh_token: str


# --- Multi-Tenant Workspace & Team Schemas ---
class WorkspaceCreate(BaseModel):
    name: str
    description: Optional[str] = None


class WorkspaceResponse(BaseModel):
    id: str
    name: str
    slug: str
    owner_id: str
    description: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class TeamCreate(BaseModel):
    workspace_id: str
    name: str
    description: Optional[str] = None


class TeamResponse(BaseModel):
    id: str
    workspace_id: str
    name: str
    description: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class InviteMemberRequest(BaseModel):
    workspace_id: str
    email: EmailStr
    role: str = "MEMBER"  # OWNER, ADMIN, MEMBER, VIEWER


class AcceptInviteRequest(BaseModel):
    invite_code: str


class InviteResponse(BaseModel):
    id: str
    workspace_id: str
    email: EmailStr
    role: str
    invite_code: str
    status: str
    expires_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True


class WorkspaceMemberResponse(BaseModel):
    id: str
    workspace_id: str
    user_id: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True



# --- User Schemas ---
class UserResponse(BaseModel):
    id: str
    email: EmailStr
    full_name: str
    role: UserRole
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None


# --- Project Schemas ---
class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None


class ProjectResponse(BaseModel):
    id: str
    user_id: str
    name: str
    description: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# --- Dataset Schemas ---
class DatasetResponse(BaseModel):
    id: str
    user_id: str
    project_id: Optional[str] = None
    name: str
    file_size: int
    row_count: int
    col_count: int
    columns_schema: Optional[Dict[str, str]] = None
    summary_stats: Optional[Dict[str, Any]] = None
    created_at: datetime

    class Config:
        from_attributes = True


class DatasetReviewRequest(BaseModel):
    target_column: Optional[str] = None


class DatasetReviewResponse(BaseModel):
    summary: Dict[str, Any]
    missing_values: Dict[str, Any]
    duplicates: Dict[str, Any]
    target_validation: Dict[str, Any]
    data_leakage: Dict[str, Any]
    outliers: Dict[str, Any]
    class_imbalance: Dict[str, Any]
    correlation_analysis: Dict[str, Any]
    ai_senior_ds_recommendation: Dict[str, Any]


class PreprocessConfigRequest(BaseModel):

    dataset_id: str
    impute_missing: Optional[bool] = True
    scaling_method: Optional[str] = "standard"  # minmax, standard, none
    encode_categorical: Optional[bool] = True
    remove_outliers: Optional[bool] = False


# --- AutoML & ML Models Schemas ---
class AutoMLStartRequest(BaseModel):
    dataset_id: str
    target_column: str
    task_type: ProblemType = ProblemType.CLASSIFICATION
    time_budget_seconds: Optional[int] = 300


class ModelResponse(BaseModel):
    id: str
    experiment_id: str
    algorithm: str
    hyperparameters: Optional[Dict[str, Any]] = None
    metrics: Optional[Dict[str, float]] = None
    artifact_path: str
    is_best_model: bool
    shap_summary: Optional[Dict[str, Any]] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ExperimentResponse(BaseModel):
    id: str
    dataset_id: str
    target_column: str
    task_type: ProblemType
    status: ExperimentStatus
    time_budget_seconds: int
    models: List[ModelResponse] = []
    created_at: datetime

    class Config:
        from_attributes = True


# --- XAI Schemas ---
class LIMESampleRequest(BaseModel):
    model_id: str
    sample_data: Dict[str, Any]


class LIMEResponse(BaseModel):
    model_id: str
    prediction: Any
    local_explanation: List[Dict[str, Any]]


# --- Prediction Schemas ---
class PredictRequest(BaseModel):
    model_id: str
    data: List[Dict[str, Any]]


class PredictResponse(BaseModel):
    model_id: str
    predictions: List[Any]
    probabilities: Optional[List[List[float]]] = None


# --- Report Schemas ---
class ReportGenerateRequest(BaseModel):
    experiment_id: str
    title: str = "Automated Machine Learning & XAI Report"
    format: str = "PDF"  # PDF, DOCX, NOTEBOOK


class ReportResponse(BaseModel):
    id: str
    experiment_id: str
    user_id: str
    title: str
    format: str
    file_path: Optional[str] = None
    content_json: Optional[Dict[str, Any]] = None
    created_at: datetime

    class Config:
        from_attributes = True


# --- Audit Log Schemas ---
class AuditLogResponse(BaseModel):
    id: str
    user_id: Optional[str] = None
    action: str
    resource: str
    details: Optional[Dict[str, Any]] = None
    ip_address: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
