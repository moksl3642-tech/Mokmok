from __future__ import annotations

from fastapi import Depends, Header, HTTPException, Request, status

from .auth import AuthService
from .crypto import InvalidTokenError
from .models import AuditLog, User
from .rate_limit import RateLimiter
from .store import InMemoryStore


class Container:
    def __init__(self) -> None:
        self.store = InMemoryStore()
        self.auth = AuthService(self.store)
        self.rate_limiter = RateLimiter()


container = Container()


def get_auth_service() -> AuthService:
    return container.auth


def get_store() -> InMemoryStore:
    return container.store


def get_rate_limiter() -> RateLimiter:
    return container.rate_limiter


def get_current_user(
    authorization: str = Header(default=""),
    auth: AuthService = Depends(get_auth_service),
) -> User:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")
    token = authorization.replace("Bearer ", "", 1)
    try:
        return auth.authenticate_access_token(token)
    except InvalidTokenError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc


def require_roles(*roles: str):
    def role_guard(user: User = Depends(get_current_user)) -> User:
        if user.role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient role")
        return user

    return role_guard


def enforce_rate_limit(
    key_prefix: str,
    *,
    limit: int,
    window_seconds: int,
):
    async def limiter(
        request: Request,
        limiter_obj: RateLimiter = Depends(get_rate_limiter),
    ) -> None:
        client_host = request.client.host if request.client else "unknown"
        key = f"{key_prefix}:{client_host}"
        if not limiter_obj.check(key, limit=limit, window_seconds=window_seconds):
            raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Rate limit exceeded")

    return limiter


def audit_admin_action(
    *,
    user: User,
    action: str,
    target: str,
    details: dict,
    store: InMemoryStore,
) -> None:
    store.insert_audit_log(
        AuditLog(
            actor_id=user.id,
            action=action,
            target=target,
            details=details,
        )
    )
