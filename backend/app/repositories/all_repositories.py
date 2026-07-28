from typing import Optional, List
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.models import (
    User, Project, Dataset, Experiment, MLModel, Prediction, Report, AuditLog
)


class UserRepository(BaseRepository[User]):
    def __init__(self, db: AsyncSession):
        super().__init__(User, db)

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalars().first()


class ProjectRepository(BaseRepository[Project]):
    def __init__(self, db: AsyncSession):
        super().__init__(Project, db)

    async def get_by_user(self, user_id: str, skip: int = 0, limit: int = 100) -> List[Project]:
        result = await self.db.execute(
            select(Project).where(Project.user_id == user_id).offset(skip).limit(limit)
        )
        return result.scalars().all()


class DatasetRepository(BaseRepository[Dataset]):
    def __init__(self, db: AsyncSession):
        super().__init__(Dataset, db)

    async def get_by_user(self, user_id: str, skip: int = 0, limit: int = 100) -> List[Dataset]:
        result = await self.db.execute(
            select(Dataset).where(Dataset.user_id == user_id).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def get_by_project(self, project_id: str) -> List[Dataset]:
        result = await self.db.execute(
            select(Dataset).where(Dataset.project_id == project_id)
        )
        return result.scalars().all()


class ExperimentRepository(BaseRepository[Experiment]):
    def __init__(self, db: AsyncSession):
        super().__init__(Experiment, db)

    async def get_with_models(self, id: str) -> Optional[Experiment]:
        result = await self.db.execute(
            select(Experiment)
            .options(selectinload(Experiment.models))
            .where(Experiment.id == id)
        )
        return result.scalars().first()

    async def get_by_dataset(self, dataset_id: str) -> List[Experiment]:
        result = await self.db.execute(
            select(Experiment)
            .options(selectinload(Experiment.models))
            .where(Experiment.dataset_id == dataset_id)
        )
        return result.scalars().all()


class ModelRepository(BaseRepository[MLModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(MLModel, db)

    async def get_best_model_for_experiment(self, experiment_id: str) -> Optional[MLModel]:
        result = await self.db.execute(
            select(MLModel)
            .where(MLModel.experiment_id == experiment_id, MLModel.is_best_model == True)
        )
        return result.scalars().first()


class PredictionRepository(BaseRepository[Prediction]):
    def __init__(self, db: AsyncSession):
        super().__init__(Prediction, db)


class ReportRepository(BaseRepository[Report]):
    def __init__(self, db: AsyncSession):
        super().__init__(Report, db)

    async def get_by_user(self, user_id: str) -> List[Report]:
        result = await self.db.execute(
            select(Report).where(Report.user_id == user_id)
        )
        return result.scalars().all()


class AuditRepository(BaseRepository[AuditLog]):
    def __init__(self, db: AsyncSession):
        super().__init__(AuditLog, db)

    async def get_recent_logs(self, limit: int = 50) -> List[AuditLog]:
        result = await self.db.execute(
            select(AuditLog).order_by(AuditLog.created_at.desc()).limit(limit)
        )
        return result.scalars().all()
