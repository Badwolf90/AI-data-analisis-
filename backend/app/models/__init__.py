import uuid
import enum
from datetime import datetime, timezone
from sqlalchemy import (
    Column, String, DateTime, Boolean, ForeignKey, Integer, BigInteger, JSON,
    Enum as SQLEnum, Index, CheckConstraint
)
from sqlalchemy.orm import relationship
from app.core.database import Base


# --- Enum Definitions ---
class UserRole(str, enum.Enum):
    ADMIN = "ADMIN"
    ANALYST = "ANALYST"
    VIEWER = "VIEWER"


class ProblemType(str, enum.Enum):
    CLASSIFICATION = "CLASSIFICATION"
    REGRESSION = "REGRESSION"


class ExperimentStatus(str, enum.Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class NotificationType(str, enum.Enum):
    INFO = "INFO"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"


def generate_uuid():
    return str(uuid.uuid4())


def current_utc():
    return datetime.now(timezone.utc)


# 1. Users Table
class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(150), nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.ANALYST, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=current_utc, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=current_utc, onupdate=current_utc, nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    projects = relationship("Project", back_populates="owner", cascade="all, delete-orphan")
    datasets = relationship("Dataset", back_populates="owner", cascade="all, delete-orphan")
    reports = relationship("Report", back_populates="user", cascade="all, delete-orphan")
    api_keys = relationship("APIKey", back_populates="user", cascade="all, delete-orphan")
    sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    logs = relationship("AuditLog", back_populates="user", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_users_email_active", "email", "is_active"),
        Index("idx_users_deleted_at", "deleted_at"),
    )


# 2. Projects Table
class Project(Base):
    __tablename__ = "projects"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    workspace_id = Column(String(36), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(512), nullable=True)
    created_at = Column(DateTime(timezone=True), default=current_utc, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=current_utc, onupdate=current_utc, nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    owner = relationship("User", back_populates="projects")
    workspace = relationship("Workspace", back_populates="projects")
    datasets = relationship("Dataset", back_populates="project", cascade="all, delete-orphan")


    __table_args__ = (
        Index("idx_projects_user_deleted", "user_id", "deleted_at"),
    )


# 3. Datasets Table
class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=True, index=True)
    name = Column(String(255), nullable=False)
    file_path = Column(String(512), nullable=False)
    file_size = Column(BigInteger, nullable=False)
    row_count = Column(Integer, default=0, nullable=False)
    col_count = Column(Integer, default=0, nullable=False)
    columns_schema = Column(JSON, nullable=True)
    summary_stats = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), default=current_utc, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=current_utc, onupdate=current_utc, nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    owner = relationship("User", back_populates="datasets")
    project = relationship("Project", back_populates="datasets")
    experiments = relationship("Experiment", back_populates="dataset", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint("file_size >= 0", name="check_dataset_file_size_positive"),
        Index("idx_datasets_user_deleted", "user_id", "deleted_at"),
    )


# 4. Experiments / History Table
class Experiment(Base):
    __tablename__ = "experiments"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    dataset_id = Column(String(36), ForeignKey("datasets.id", ondelete="CASCADE"), nullable=False, index=True)
    target_column = Column(String(128), nullable=False)
    task_type = Column(SQLEnum(ProblemType), default=ProblemType.CLASSIFICATION, nullable=False)
    status = Column(SQLEnum(ExperimentStatus), default=ExperimentStatus.PENDING, nullable=False, index=True)
    time_budget_seconds = Column(Integer, default=300, nullable=False)
    created_at = Column(DateTime(timezone=True), default=current_utc, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=current_utc, onupdate=current_utc, nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    dataset = relationship("Dataset", back_populates="experiments")
    models = relationship("MLModel", back_populates="experiment", cascade="all, delete-orphan")
    reports = relationship("Report", back_populates="experiment", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_experiments_dataset_status", "dataset_id", "status"),
    )


# 5. Models Table
class MLModel(Base):
    __tablename__ = "models"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    experiment_id = Column(String(36), ForeignKey("experiments.id", ondelete="CASCADE"), nullable=False, index=True)
    algorithm = Column(String(100), nullable=False)
    hyperparameters = Column(JSON, nullable=True)
    metrics = Column(JSON, nullable=True)
    artifact_path = Column(String(512), nullable=False)
    is_best_model = Column(Boolean, default=False, nullable=False, index=True)
    shap_summary = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), default=current_utc, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=current_utc, onupdate=current_utc, nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    experiment = relationship("Experiment", back_populates="models")
    predictions = relationship("Prediction", back_populates="model", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_models_experiment_best", "experiment_id", "is_best_model"),
    )


# 6. Predictions Table
class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    model_id = Column(String(36), ForeignKey("models.id", ondelete="CASCADE"), nullable=False, index=True)
    input_data = Column(JSON, nullable=False)
    prediction_result = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), default=current_utc, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=current_utc, onupdate=current_utc, nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    model = relationship("MLModel", back_populates="predictions")


# 7. Reports Table
class Report(Base):
    __tablename__ = "reports"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    experiment_id = Column(String(36), ForeignKey("experiments.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    format = Column(String(20), default="PDF", nullable=False)
    file_path = Column(String(512), nullable=True)
    content_json = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), default=current_utc, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=current_utc, onupdate=current_utc, nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="reports")
    experiment = relationship("Experiment", back_populates="reports")


# 8. Logs (Audit Log) Table
class AuditLog(Base):
    __tablename__ = "logs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    action = Column(String(100), nullable=False, index=True)
    resource = Column(String(100), nullable=False)
    details = Column(JSON, nullable=True)
    ip_address = Column(String(45), nullable=True)
    created_at = Column(DateTime(timezone=True), default=current_utc, nullable=False, index=True)

    user = relationship("User", back_populates="logs")


# 9. API Keys Table
class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    key_name = Column(String(100), nullable=False)
    hashed_key = Column(String(255), nullable=False, unique=True)
    prefix = Column(String(16), nullable=False, index=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=current_utc, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=current_utc, onupdate=current_utc, nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="api_keys")

    __table_args__ = (
        Index("idx_api_keys_prefix_active", "prefix", "is_active"),
    )


# 10. Sessions Table
class UserSession(Base):
    __tablename__ = "sessions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    refresh_token = Column(String(512), nullable=False, unique=True, index=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(255), nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_revoked = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), default=current_utc, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=current_utc, onupdate=current_utc, nullable=False)

    user = relationship("User", back_populates="sessions")


class WorkspaceRole(str, enum.Enum):
    OWNER = "OWNER"
    ADMIN = "ADMIN"
    MEMBER = "MEMBER"
    VIEWER = "VIEWER"


class TeamRole(str, enum.Enum):
    LEAD = "LEAD"
    MEMBER = "MEMBER"
    VIEWER = "VIEWER"


class InviteStatus(str, enum.Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    EXPIRED = "EXPIRED"
    REVOKED = "REVOKED"


# 12. Workspace Table (Top-level Multi-tenant Isolation Container)
class Workspace(Base):
    __tablename__ = "workspaces"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    slug = Column(String(100), unique=True, index=True, nullable=False)
    owner_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    description = Column(String(512), nullable=True)
    created_at = Column(DateTime(timezone=True), default=current_utc, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=current_utc, onupdate=current_utc, nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    owner = relationship("User", foreign_keys=[owner_id])
    members = relationship("WorkspaceMember", back_populates="workspace", cascade="all, delete-orphan")
    teams = relationship("Team", back_populates="workspace", cascade="all, delete-orphan")
    invites = relationship("Invite", back_populates="workspace", cascade="all, delete-orphan")
    projects = relationship("Project", back_populates="workspace", cascade="all, delete-orphan")


# 13. Workspace Member Table (RBAC Roles for Workspaces)
class WorkspaceMember(Base):
    __tablename__ = "workspace_members"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    workspace_id = Column(String(36), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(SQLEnum(WorkspaceRole), default=WorkspaceRole.MEMBER, nullable=False)
    created_at = Column(DateTime(timezone=True), default=current_utc, nullable=False)

    workspace = relationship("Workspace", back_populates="members")
    user = relationship("User")

    __table_args__ = (
        Index("idx_workspace_user_unique", "workspace_id", "user_id", unique=True),
    )


# 14. Team Table
class Team(Base):
    __tablename__ = "teams"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    workspace_id = Column(String(36), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(512), nullable=True)
    created_at = Column(DateTime(timezone=True), default=current_utc, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=current_utc, onupdate=current_utc, nullable=False)

    workspace = relationship("Workspace", back_populates="teams")
    members = relationship("TeamMember", back_populates="team", cascade="all, delete-orphan")


# 15. Team Member Table
class TeamMember(Base):
    __tablename__ = "team_members"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    team_id = Column(String(36), ForeignKey("teams.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(SQLEnum(TeamRole), default=TeamRole.MEMBER, nullable=False)
    created_at = Column(DateTime(timezone=True), default=current_utc, nullable=False)

    team = relationship("Team", back_populates="members")
    user = relationship("User")

    __table_args__ = (
        Index("idx_team_user_unique", "team_id", "user_id", unique=True),
    )


# 16. Invite Table (Team & Workspace Member Invites)
class Invite(Base):
    __tablename__ = "invites"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    workspace_id = Column(String(36), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    email = Column(String(255), nullable=False, index=True)
    role = Column(SQLEnum(WorkspaceRole), default=WorkspaceRole.MEMBER, nullable=False)
    invite_code = Column(String(64), unique=True, index=True, nullable=False)
    status = Column(SQLEnum(InviteStatus), default=InviteStatus.PENDING, nullable=False)
    invited_by_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), default=current_utc, nullable=False)

    workspace = relationship("Workspace", back_populates="invites")
    invited_by = relationship("User")

