from __future__ import annotations

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel

from .security.auth import AuthService
from .security.crypto import InvalidTokenError
from .security.dependencies import (
    audit_admin_action,
    container,
    enforce_rate_limit,
    get_auth_service,
    get_current_user,
    get_store,
    require_roles,
)
from .security.models import User
from .security.store import InMemoryStore

app = FastAPI(title="Mokmok Backend")


class LoginRequest(BaseModel):
    username: str
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class HandInputRequest(BaseModel):
    value: str


class ConfigPatchRequest(BaseModel):
    maintenance_mode: bool


@app.on_event("startup")
def bootstrap_users() -> None:
    if container.store.get_user_by_username("admin") is None:
        container.auth.create_user(1, "admin", "admin123", "admin")
    if container.store.get_user_by_username("user") is None:
        container.auth.create_user(2, "user", "user123", "user")


@app.post(
    "/auth/login",
    dependencies=[Depends(enforce_rate_limit("login", limit=5, window_seconds=60))],
)
def login(payload: LoginRequest, auth: AuthService = Depends(get_auth_service)) -> dict[str, str]:
    try:
        return auth.login(payload.username, payload.password)
    except InvalidTokenError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc


@app.post(
    "/auth/session/refresh",
    dependencies=[Depends(enforce_rate_limit("create-session", limit=8, window_seconds=60))],
)
def refresh_session(payload: RefreshRequest, auth: AuthService = Depends(get_auth_service)) -> dict[str, str]:
    try:
        return auth.rotate_refresh_token(payload.refresh_token)
    except InvalidTokenError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc


@app.post("/auth/session/revoke")
def revoke_session(payload: RefreshRequest, auth: AuthService = Depends(get_auth_service)) -> dict[str, str]:
    try:
        auth.revoke_session(payload.refresh_token, reason="user-logout")
    except InvalidTokenError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc
    return {"status": "revoked"}


@app.post(
    "/hands/input",
    dependencies=[Depends(enforce_rate_limit("hand-input", limit=10, window_seconds=60))],
)
def hand_input(_: HandInputRequest, user: User = Depends(get_current_user)) -> dict[str, str]:
    return {"status": f"accepted-by-{user.username}"}


@app.get("/admin/users", dependencies=[Depends(require_roles("admin"))])
def admin_list_users(store: InMemoryStore = Depends(get_store)) -> dict[str, list[str]]:
    return {"users": sorted(store.users_by_username.keys())}


@app.patch("/admin/system/config", dependencies=[Depends(require_roles("admin"))])
def admin_patch_system_config(
    payload: ConfigPatchRequest,
    user: User = Depends(get_current_user),
    store: InMemoryStore = Depends(get_store),
) -> dict[str, bool]:
    audit_admin_action(
        user=user,
        action="system.config.update",
        target="system.config",
        details={"maintenance_mode": payload.maintenance_mode},
        store=store,
    )
    return {"maintenance_mode": payload.maintenance_mode}


@app.get("/admin/audit-logs", dependencies=[Depends(require_roles("admin"))])
def admin_audit_logs(store: InMemoryStore = Depends(get_store)) -> dict[str, list[dict]]:
    return {
        "logs": [
            {
                "actor_id": item.actor_id,
                "action": item.action,
                "target": item.target,
                "details": item.details,
                "created_at": item.created_at.isoformat(),
            }
            for item in store.audit_logs
        ]
    }


@app.get("/permissions/matrix")
def permission_matrix() -> dict[str, dict[str, str]]:
    return {
        "/auth/login": {"anonymous": "allow", "user": "allow", "admin": "allow"},
        "/auth/session/refresh": {"anonymous": "allow-with-refresh-token", "user": "allow", "admin": "allow"},
        "/auth/session/revoke": {"anonymous": "allow-with-refresh-token", "user": "allow", "admin": "allow"},
        "/hands/input": {"anonymous": "deny", "user": "allow", "admin": "allow"},
        "/admin/users": {"anonymous": "deny", "user": "deny", "admin": "allow"},
        "/admin/system/config": {"anonymous": "deny", "user": "deny", "admin": "allow+audit"},
        "/admin/audit-logs": {"anonymous": "deny", "user": "deny", "admin": "allow"},
    }
from fastapi import FastAPI

from app.api.v1.routers.game import router as game_router

app = FastAPI(title="Mokmok Backend")
app.include_router(game_router, prefix="/api/v1")
