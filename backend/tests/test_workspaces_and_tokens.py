import uuid
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_auth_refresh_token_rotation():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        email = f"user_{uuid.uuid4().hex[:8]}@example.com"
        reg_payload = {
            "email": email,
            "password": "Password123!",
            "full_name": "Enterprise User"
        }
        res_reg = await ac.post("/api/v1/auth/register", json=reg_payload)
        assert res_reg.status_code == 201

        # Login
        login_res = await ac.post("/api/v1/auth/login", json={
            "email": email,
            "password": "Password123!"
        })
        assert login_res.status_code == 200
        data = login_res.json()
        access_token = data["access_token"]
        refresh_token = data["refresh_token"]

        # Refresh Token Exchange
        ref_res = await ac.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token})
        assert ref_res.status_code == 200
        ref_data = ref_res.json()
        assert "access_token" in ref_data
        assert "refresh_token" in ref_data
        assert ref_data["refresh_token"] != refresh_token  # Token rotation


@pytest.mark.asyncio
async def test_workspace_team_invite_rbac_flow():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        owner_email = f"owner_{uuid.uuid4().hex[:8]}@acme.com"
        member_email = f"member_{uuid.uuid4().hex[:8]}@acme.com"

        # Register Owner
        await ac.post("/api/v1/auth/register", json={
            "email": owner_email,
            "password": "Password123!",
            "full_name": "Acme Owner"
        })
        login_res = await ac.post("/api/v1/auth/login", json={"email": owner_email, "password": "Password123!"})
        headers_owner = {"Authorization": f"Bearer {login_res.json()['access_token']}"}

        # Create Workspace
        ws_res = await ac.post("/api/v1/workspaces", json={"name": "Acme Global Analytics", "description": "Multi-tenant workspace"}, headers=headers_owner)
        assert ws_res.status_code == 201
        ws = ws_res.json()
        ws_id = ws["id"]

        # Create Team
        team_res = await ac.post("/api/v1/workspaces/teams", json={"workspace_id": ws_id, "name": "AI Engineers"}, headers=headers_owner)
        assert team_res.status_code == 201

        # Invite Member
        invite_res = await ac.post("/api/v1/workspaces/invites", json={"workspace_id": ws_id, "email": member_email, "role": "MEMBER"}, headers=headers_owner)
        assert invite_res.status_code == 201
        invite_code = invite_res.json()["invite_code"]

        # Register Member
        await ac.post("/api/v1/auth/register", json={
            "email": member_email,
            "password": "Password123!",
            "full_name": "Acme Member"
        })
        login_member = await ac.post("/api/v1/auth/login", json={"email": member_email, "password": "Password123!"})
        headers_member = {"Authorization": f"Bearer {login_member.json()['access_token']}"}

        # Accept Invite
        accept_res = await ac.post("/api/v1/workspaces/invites/accept", json={"invite_code": invite_code}, headers=headers_member)
        assert accept_res.status_code == 200

        # List Workspace Members
        members_res = await ac.get(f"/api/v1/workspaces/{ws_id}/members", headers=headers_member)
        assert members_res.status_code == 200
        assert len(members_res.json()) >= 2

