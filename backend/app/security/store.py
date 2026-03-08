from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone

from .models import AuditLog, SessionToken, User


class InMemoryStore:
    """Simple in-memory persistence for demo/testing."""

    def __init__(self) -> None:
        self.users_by_id: dict[int, User] = {}
        self.users_by_username: dict[str, User] = {}
        self.tokens: dict[str, SessionToken] = {}
        self.user_tokens: dict[int, set[str]] = defaultdict(set)
        self.audit_logs: list[AuditLog] = []  # mirrors system.audit_logs

    def add_user(self, user: User) -> None:
        self.users_by_id[user.id] = user
        self.users_by_username[user.username] = user

    def get_user_by_username(self, username: str) -> User | None:
        return self.users_by_username.get(username)

    def get_user_by_id(self, user_id: int) -> User | None:
        return self.users_by_id.get(user_id)

    def save_token(self, token: SessionToken) -> None:
        self.tokens[token.jti] = token
        self.user_tokens[token.user_id].add(token.jti)

    def get_token(self, jti: str) -> SessionToken | None:
        return self.tokens.get(jti)

    def revoke_token(self, jti: str, reason: str) -> None:
        token = self.tokens.get(jti)
        if token is not None:
            token.revoked = True
            token.revoked_reason = reason

    def revoke_descendants(self, parent_jti: str, reason: str) -> None:
        for token in self.tokens.values():
            if token.parent_jti == parent_jti:
                token.revoked = True
                token.revoked_reason = reason

    def active_user_tokens(self, user_id: int) -> list[SessionToken]:
        now = datetime.now(timezone.utc)
        return [
            self.tokens[jti]
            for jti in self.user_tokens.get(user_id, set())
            if self.tokens[jti].expires_at > now and not self.tokens[jti].revoked
        ]

    def insert_audit_log(self, log: AuditLog) -> None:
        # Equivalent to INSERT INTO system.audit_logs (...)
        self.audit_logs.append(log)
