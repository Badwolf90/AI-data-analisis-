import os
import json
import joblib
import pandas as pd
import numpy as np
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone, timedelta
from fastapi import HTTPException, status, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import get_password_hash, verify_password, create_access_token, create_refresh_token
from app.core.logging import logger

from app.models import ProblemType, ExperimentStatus, WorkspaceRole, TeamRole, InviteStatus
from app.repositories import (
    UserRepository, ProjectRepository, DatasetRepository,
    ExperimentRepository, ModelRepository, PredictionRepository,
    ReportRepository, AuditRepository, UserSessionRepository,
    WorkspaceRepository, WorkspaceMemberRepository, TeamRepository,
    TeamMemberRepository, InviteRepository
)
from app.automl_engine.dataset_reviewer import DatasetReviewerEngine
from app.schemas import (
    RegisterRequest, LoginRequest, TokenResponse, ProjectCreate, PreprocessConfigRequest,
    AutoMLStartRequest, LIMESampleRequest, PredictRequest, ReportGenerateRequest,
    WorkspaceCreate, TeamCreate, InviteMemberRequest, AcceptInviteRequest, RefreshTokenRequest,
    DatasetReviewRequest, DatasetReviewResponse
)



# ML Libraries
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, mean_squared_error, r2_score
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, LabelEncoder
import optuna

# Disable optuna verbosity in logs
optuna.logging.set_verbosity(optuna.logging.WARNING)


class AuthService:
    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepository(db)
        self.audit_repo = AuditRepository(db)

    async def register(self, req: RegisterRequest, ip_address: str = None):
        existing_user = await self.user_repo.get_by_email(req.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists."
            )
        hashed_password = get_password_hash(req.password)
        user_dict = {
            "email": req.email,
            "password_hash": hashed_password,
            "full_name": req.full_name,
            "role": req.role
        }
        user = await self.user_repo.create(user_dict)
        await self.audit_repo.create({
            "user_id": user.id,
            "action": "USER_REGISTER",
            "resource": "User",
            "details": {"email": user.email},
            "ip_address": ip_address
        })
        return user

    async def authenticate(self, req: LoginRequest, ip_address: str = None) -> TokenResponse:
        user = await self.user_repo.get_by_email(req.email)
        if not user or not verify_password(req.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password."
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user account."
            )
        
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        # Store Refresh Token Session for revocation and security auditing
        session_repo = UserSessionRepository(self.user_repo.db)
        await session_repo.create({
            "user_id": user.id,
            "refresh_token": refresh_token,
            "ip_address": ip_address,
            "expires_at": datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        })

        await self.audit_repo.create({
            "user_id": user.id,
            "action": "USER_LOGIN",
            "resource": "Auth",
            "details": {"email": user.email},
            "ip_address": ip_address
        })

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )

    async def refresh_token(self, refresh_token_str: str, ip_address: str = None) -> TokenResponse:
        from app.core.security import decode_token
        payload = decode_token(refresh_token_str)
        if not payload or payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token."
            )

        user_id = payload.get("sub")
        session_repo = UserSessionRepository(self.user_repo.db)
        session = await session_repo.get_by_token(refresh_token_str)

        if not session or session.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token session revoked or invalid."
            )

        # Token Rotation: Revoke old session and issue new pair
        await session_repo.update(session, {"is_revoked": True})

        new_access_token = create_access_token(user_id)
        new_refresh_token = create_refresh_token(user_id)

        await session_repo.create({
            "user_id": user_id,
            "refresh_token": new_refresh_token,
            "ip_address": ip_address,
            "expires_at": datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        })

        return TokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            token_type="bearer"
        )



class ProjectService:
    def __init__(self, db: AsyncSession):
        self.project_repo = ProjectRepository(db)

    async def create_project(self, user_id: str, req: ProjectCreate):
        project_dict = {
            "user_id": user_id,
            "name": req.name,
            "description": req.description
        }
        return await self.project_repo.create(project_dict)

    async def list_user_projects(self, user_id: str):
        return await self.project_repo.get_by_user(user_id)

    async def get_project(self, project_id: str):
        project = await self.project_repo.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return project


class DatasetService:
    def __init__(self, db: AsyncSession):
        self.dataset_repo = DatasetRepository(db)

    async def upload_dataset(self, user_id: str, file: UploadFile, project_id: Optional[str] = None):
        if not file.filename.endswith(('.csv', '.xlsx', '.parquet')):
            raise HTTPException(status_code=400, detail="Only CSV, XLSX, and Parquet files are supported.")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(settings.UPLOAD_DIR, safe_filename)

        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)

        # Read dataset and compute EDA
        try:
            if file.filename.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file.filename.endswith('.parquet'):
                df = pd.read_parquet(file_path)
            else:
                df = pd.read_excel(file_path)
        except Exception as e:
            os.remove(file_path)
            raise HTTPException(status_code=400, detail=f"Error reading file content: {str(e)}")

        row_count, col_count = df.shape
        columns_schema = {col: str(dtype) for col, dtype in df.dtypes.items()}
        
        # Calculate summary statistics
        stats = {}
        for col in df.columns:
            stats[col] = {
                "null_count": int(df[col].isnull().sum()),
                "unique_count": int(df[col].nunique()),
                "dtype": str(df[col].dtype)
            }
            if pd.api.types.is_numeric_dtype(df[col]):
                stats[col].update({
                    "mean": float(df[col].mean()) if not pd.isna(df[col].mean()) else 0.0,
                    "std": float(df[col].std()) if not pd.isna(df[col].std()) else 0.0,
                    "min": float(df[col].min()) if not pd.isna(df[col].min()) else 0.0,
                    "max": float(df[col].max()) if not pd.isna(df[col].max()) else 0.0
                })

        dataset_dict = {
            "user_id": user_id,
            "project_id": project_id,
            "name": file.filename,
            "file_path": file_path,
            "file_size": len(content),
            "row_count": row_count,
            "col_count": col_count,
            "columns_schema": columns_schema,
            "summary_stats": stats
        }
        return await self.dataset_repo.create(dataset_dict)

    async def get_dataset(self, dataset_id: str):
        dataset = await self.dataset_repo.get_by_id(dataset_id)
        if not dataset:
            raise HTTPException(status_code=404, detail="Dataset not found")
        return dataset

    async def review_dataset(self, dataset_id: str, target_column: Optional[str] = None):
        dataset = await self.get_dataset(dataset_id)
        file_path = dataset.file_path

        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith('.parquet'):
                df = pd.read_parquet(file_path)
            else:
                df = pd.read_excel(file_path)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error loading dataset for audit: {str(e)}")

        return DatasetReviewerEngine.audit_dataset(df, target_column=target_column)


    async def preprocess_dataset(self, req: PreprocessConfigRequest):
        dataset = await self.get_dataset(req.dataset_id)
        df = pd.read_csv(dataset.file_path)

        # Impute missing values
        if req.impute_missing:
            num_cols = df.select_dtypes(include=[np.number]).columns
            cat_cols = df.select_dtypes(exclude=[np.number]).columns
            if len(num_cols) > 0:
                imp_num = SimpleImputer(strategy="median")
                df[num_cols] = imp_num.fit_transform(df[num_cols])
            if len(cat_cols) > 0:
                imp_cat = SimpleImputer(strategy="most_frequent")
                df[cat_cols] = imp_cat.fit_transform(df[cat_cols])

        # Encoding
        if req.encode_categorical:
            cat_cols = df.select_dtypes(exclude=[np.number]).columns
            for col in cat_cols:
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col].astype(str))

        # Scaling
        if req.scaling_method == "standard":
            num_cols = df.select_dtypes(include=[np.number]).columns
            scaler = StandardScaler()
            df[num_cols] = scaler.fit_transform(df[num_cols])

        # Save cleaned file
        cleaned_file_path = dataset.file_path.replace(".csv", "_cleaned.csv")
        df.to_csv(cleaned_file_path, index=False)
        
        return {
            "message": "Dataset successfully preprocessed.",
            "cleaned_file_path": cleaned_file_path,
            "rows": len(df),
            "cols": len(df.columns)
        }


from app.automl_engine.engine import AutoMLEngine


class AutoMLService:
    """
    Application Service for AutoML Orchestration.
    Follows Clean Architecture & SOLID (SRP/DIP): Delegates domain ML execution 
    to AutoMLEngine while handling transaction lifecycle and repository persistence.
    """
    def __init__(self, db: AsyncSession, engine_cls=None):
        self.exp_repo = ExperimentRepository(db)
        self.model_repo = ModelRepository(db)
        self.dataset_repo = DatasetRepository(db)
        self.engine_cls = engine_cls or AutoMLEngine

    async def run_automl(self, req: AutoMLStartRequest) -> Any:
        dataset = await self.dataset_repo.get_by_id(req.dataset_id)
        if not dataset:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Dataset not found."
            )

        # 1. Create Initial Experiment Entry with RUNNING status
        exp = await self.exp_repo.create({
            "dataset_id": req.dataset_id,
            "target_column": req.target_column,
            "task_type": req.task_type,
            "status": ExperimentStatus.RUNNING,
            "time_budget_seconds": req.time_budget_seconds or 300
        })

        try:
            # 2. Ingest Dataset
            if not os.path.exists(dataset.file_path):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Dataset file missing on server disk."
                )

            if dataset.file_path.endswith('.parquet'):
                df = pd.read_parquet(dataset.file_path)
            elif dataset.file_path.endswith('.xlsx'):
                df = pd.read_excel(dataset.file_path)
            else:
                df = pd.read_csv(dataset.file_path)

            if req.target_column not in df.columns:
                raise ValueError(f"Target column '{req.target_column}' not found in dataset columns.")

            # 3. Instantiate Domain AutoML Engine via Dependency Injection
            engine = self.engine_cls(experiment_id=exp.id)
            automl_report = engine.run_full_automl(
                df=df,
                target_column=req.target_column,
                n_trials_per_model=3
            )

            # 4. Map Engine Leaderboard Entries to Model Database Records
            leaderboard = automl_report.get("leaderboard", [])
            for item in leaderboard:
                algo_name = item.get("algorithm", "UnknownAlgorithm")
                metrics = item.get("metrics", {})
                is_best = item.get("is_best", False)
                artifact_path = item.get("artifact_path", "")
                hyperparams = item.get("hyperparameters", {})
                shap_summary = item.get("shap_summary", {})

                await self.model_repo.create({
                    "experiment_id": exp.id,
                    "algorithm": algo_name,
                    "hyperparameters": hyperparams,
                    "metrics": metrics,
                    "artifact_path": artifact_path,
                    "is_best_model": is_best,
                    "shap_summary": shap_summary
                })

            # 5. Transition Experiment Status to COMPLETED
            await self.exp_repo.update(exp, {"status": ExperimentStatus.COMPLETED})
            return await self.exp_repo.get_with_models(exp.id)

        except Exception as e:
            logger.error(f"AutoML Training Error for Experiment {exp.id}: {str(e)}")
            await self.exp_repo.update(exp, {"status": ExperimentStatus.FAILED})
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"AutoML execution failed: {str(e)}"
            )



class XAIService:
    def __init__(self, db: AsyncSession):
        self.model_repo = ModelRepository(db)

    async def get_global_shap(self, model_id: str):
        model = await self.model_repo.get_by_id(model_id)
        if not model:
            raise HTTPException(status_code=404, detail="Model not found")
        
        return {
            "model_id": model.id,
            "algorithm": model.algorithm,
            "feature_importance_shap": model.shap_summary or {}
        }

    async def get_lime_local_explanation(self, req: LIMESampleRequest):
        model_obj = await self.model_repo.get_by_id(req.model_id)
        if not model_obj or not os.path.exists(model_obj.artifact_path):
            raise HTTPException(status_code=404, detail="Model artifact not found")

        model = joblib.load(model_obj.artifact_path)
        sample_df = pd.DataFrame([req.sample_data])
        
        # Predict sample
        pred = model.predict(sample_df)[0]
        
        # Generate simulated local contribution weights
        explanations = []
        for col, val in req.sample_data.items():
            explanations.append({
                "feature": col,
                "value": val,
                "contribution_score": round(float(np.random.uniform(-0.3, 0.3)), 4)
            })

        return {
            "model_id": req.model_id,
            "prediction": int(pred) if isinstance(pred, (np.integer, int)) else float(pred),
            "local_explanation": sorted(explanations, key=lambda x: abs(x["contribution_score"]), reverse=True)
        }


class PredictionService:
    def __init__(self, db: AsyncSession):
        self.model_repo = ModelRepository(db)
        self.pred_repo = PredictionRepository(db)

    async def predict(self, req: PredictRequest):
        model_obj = await self.model_repo.get_by_id(req.model_id)
        if not model_obj or not os.path.exists(model_obj.artifact_path):
            raise HTTPException(status_code=404, detail="Model artifact not found.")

        model = joblib.load(model_obj.artifact_path)
        df_input = pd.DataFrame(req.data)

        predictions = model.predict(df_input).tolist()
        probabilities = None
        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(df_input).tolist()

        pred_record = await self.pred_repo.create({
            "model_id": req.model_id,
            "input_data": req.data,
            "prediction_result": {"predictions": predictions, "probabilities": probabilities}
        })

        return {
            "prediction_id": pred_record.id,
            "model_id": req.model_id,
            "predictions": predictions,
            "probabilities": probabilities
        }


class ReportService:
    def __init__(self, db: AsyncSession):
        self.report_repo = ReportRepository(db)
        self.exp_repo = ExperimentRepository(db)

    async def generate_report(self, user_id: str, req: ReportGenerateRequest):
        exp = await self.exp_repo.get_with_models(req.experiment_id)
        if not exp:
            raise HTTPException(status_code=404, detail="Experiment not found")

        report_content = {
            "title": req.title,
            "experiment_id": exp.id,
            "target_column": exp.target_column,
            "task_type": exp.task_type,
            "status": exp.status,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "models_summary": [
                {
                    "algorithm": m.algorithm,
                    "is_best": m.is_best_model,
                    "metrics": m.metrics
                } for m in exp.models
            ]
        }

        report_file_name = f"report_{exp.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_path = os.path.join(settings.REPORT_DIR, report_file_name)

        with open(report_path, "w") as f:
            json.dump(report_content, f, indent=2)

        return await self.report_repo.create({
            "user_id": user_id,
            "experiment_id": exp.id,
            "title": req.title,
            "format": req.format,
            "file_path": report_path,
            "content_json": report_content
        })


import secrets


class WorkspaceService:
    """
    Enterprise Multi-Tenant Workspace & Team Service.
    Handles multi-tenant resource isolation, workspace membership, teams,
    role-based access control (RBAC), and email/code member invitations.
    """
    def __init__(self, db: AsyncSession):
        self.db = db
        self.workspace_repo = WorkspaceRepository(db)
        self.member_repo = WorkspaceMemberRepository(db)
        self.team_repo = TeamRepository(db)
        self.invite_repo = InviteRepository(db)
        self.user_repo = UserRepository(db)

    async def create_workspace(self, user_id: str, req: WorkspaceCreate):
        slug = req.name.lower().replace(" ", "-") + "-" + secrets.token_hex(3)
        workspace = await self.workspace_repo.create({
            "name": req.name,
            "slug": slug,
            "owner_id": user_id,
            "description": req.description
        })

        # Add creator as Workspace OWNER
        await self.member_repo.create({
            "workspace_id": workspace.id,
            "user_id": user_id,
            "role": WorkspaceRole.OWNER
        })

        return workspace

    async def list_user_workspaces(self, user_id: str):
        return await self.workspace_repo.get_user_workspaces(user_id)

    async def create_team(self, user_id: str, req: TeamCreate):
        # Verify workspace membership & permission
        member = await self.member_repo.get_member(req.workspace_id, user_id)
        if not member or member.role not in [WorkspaceRole.OWNER, WorkspaceRole.ADMIN]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions to create team in this workspace."
            )

        return await self.team_repo.create({
            "workspace_id": req.workspace_id,
            "name": req.name,
            "description": req.description
        })

    async def invite_member(self, invited_by_id: str, req: InviteMemberRequest):
        member = await self.member_repo.get_member(req.workspace_id, invited_by_id)
        if not member or member.role not in [WorkspaceRole.OWNER, WorkspaceRole.ADMIN]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only workspace Owners or Admins can invite new members."
            )

        invite_code = secrets.token_urlsafe(16)
        expires_at = datetime.now(timezone.utc) + timedelta(days=7)

        return await self.invite_repo.create({
            "workspace_id": req.workspace_id,
            "email": req.email,
            "role": req.role,
            "invite_code": invite_code,
            "invited_by_id": invited_by_id,
            "status": InviteStatus.PENDING,
            "expires_at": expires_at
        })

    async def accept_invite(self, user_id: str, req: AcceptInviteRequest):
        invite = await self.invite_repo.get_by_code(req.invite_code)
        if not invite or invite.status != InviteStatus.PENDING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid, expired, or already accepted invitation code."
            )

        expires_at = invite.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)

        if expires_at < datetime.now(timezone.utc):
            await self.invite_repo.update(invite, {"status": InviteStatus.EXPIRED})
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invitation code has expired."
            )


        # Check if already a member
        existing_member = await self.member_repo.get_member(invite.workspace_id, user_id)
        if not existing_member:
            await self.member_repo.create({
                "workspace_id": invite.workspace_id,
                "user_id": user_id,
                "role": invite.role
            })

        await self.invite_repo.update(invite, {"status": InviteStatus.ACCEPTED})
        return {"message": "Successfully joined workspace.", "workspace_id": invite.workspace_id}

    async def list_workspace_members(self, workspace_id: str, user_id: str):
        member = await self.member_repo.get_member(workspace_id, user_id)
        if not member:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not a member of this workspace."
            )
        return await self.member_repo.list_members(workspace_id)

