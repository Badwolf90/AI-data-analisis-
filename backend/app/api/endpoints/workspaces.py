from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models import User
from app.schemas import (
    WorkspaceCreate, WorkspaceResponse, TeamCreate, TeamResponse,
    InviteMemberRequest, InviteResponse, AcceptInviteRequest, WorkspaceMemberResponse
)
from app.services import WorkspaceService

router = APIRouter()


def get_workspace_service(db: AsyncSession = Depends(get_db)) -> WorkspaceService:
    return WorkspaceService(db)


@router.post("", response_model=WorkspaceResponse, status_code=status.HTTP_201_CREATED)
async def create_workspace(
    req: WorkspaceCreate,
    current_user: User = Depends(get_current_user),
    service: WorkspaceService = Depends(get_workspace_service)
):
    """
    Creates a new multi-tenant workspace and assigns the creator as Workspace OWNER.
    """
    return await service.create_workspace(current_user.id, req)


@router.get("", response_model=List[WorkspaceResponse])
async def list_workspaces(
    current_user: User = Depends(get_current_user),
    service: WorkspaceService = Depends(get_workspace_service)
):
    """
    Lists all workspaces where the authenticated user is a member.
    """
    return await service.list_user_workspaces(current_user.id)


@router.post("/teams", response_model=TeamResponse, status_code=status.HTTP_201_CREATED)
async def create_team(
    req: TeamCreate,
    current_user: User = Depends(get_current_user),
    service: WorkspaceService = Depends(get_workspace_service)
):
    """
    Creates a sub-team within a workspace (Requires OWNER or ADMIN permission).
    """
    return await service.create_team(current_user.id, req)


@router.post("/invites", response_model=InviteResponse, status_code=status.HTTP_201_CREATED)
async def invite_member(
    req: InviteMemberRequest,
    current_user: User = Depends(get_current_user),
    service: WorkspaceService = Depends(get_workspace_service)
):
    """
    Generates a member invite code to join a workspace with a specified role (OWNER, ADMIN, MEMBER, VIEWER).
    """
    return await service.invite_member(current_user.id, req)


@router.post("/invites/accept", status_code=status.HTTP_200_OK)
async def accept_invite(
    req: AcceptInviteRequest,
    current_user: User = Depends(get_current_user),
    service: WorkspaceService = Depends(get_workspace_service)
):
    """
    Accepts an invitation code and adds the authenticated user as a member of the workspace.
    """
    return await service.accept_invite(current_user.id, req)


@router.get("/{workspace_id}/members", response_model=List[WorkspaceMemberResponse])
async def list_members(
    workspace_id: str,
    current_user: User = Depends(get_current_user),
    service: WorkspaceService = Depends(get_workspace_service)
):
    """
    Lists all members and their assigned RBAC roles for a given workspace.
    """
    return await service.list_workspace_members(workspace_id, current_user.id)
