from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(slots=True)
class User:
    id: int
    username: str
    password_hash: str
    role: str
    is_active: bool = True


@dataclass(slots=True)
class SessionToken:
    jti: str
    user_id: int
    parent_jti: str | None
    token_type: str
    expires_at: datetime
    revoked: bool = False
    revoked_reason: str | None = None


@dataclass(slots=True)
class AuditLog:
    actor_id: int
    action: str
    target: str
    details: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
