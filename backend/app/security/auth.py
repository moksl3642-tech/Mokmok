from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from .crypto import InvalidTokenError, create_jwt, decode_jwt, hash_password, verify_password
from .models import SessionToken, User
from .store import InMemoryStore


@dataclass(frozen=True, slots=True)
class AuthConfig:
    jwt_secret: str = "dev-secret"
    access_ttl: timedelta = timedelta(minutes=15)
    refresh_ttl: timedelta = timedelta(days=7)


class AuthService:
    def __init__(self, store: InMemoryStore, config: AuthConfig | None = None) -> None:
        self.store = store
        self.config = config or AuthConfig()

    def create_user(self, user_id: int, username: str, password: str, role: str) -> User:
        user = User(id=user_id, username=username, password_hash=hash_password(password), role=role)
        self.store.add_user(user)
        return user

    def login(self, username: str, password: str) -> dict[str, str]:
        user = self.store.get_user_by_username(username)
        if not user or not user.is_active or not verify_password(password, user.password_hash):
            raise InvalidTokenError("Invalid credentials")
        return self._issue_token_pair(user.id, parent_jti=None)

    def _issue_token_pair(self, user_id: int, *, parent_jti: str | None) -> dict[str, str]:
        refresh_token = create_jwt(
            secret=self.config.jwt_secret,
            subject=user_id,
            token_type="refresh",
            expires_delta=self.config.refresh_ttl,
            parent_jti=parent_jti,
        )
        refresh_payload = decode_jwt(refresh_token, secret=self.config.jwt_secret, expected_type="refresh")
        self.store.save_token(
            SessionToken(
                jti=refresh_payload["jti"],
                user_id=user_id,
                parent_jti=parent_jti,
                token_type="refresh",
                expires_at=datetime.fromtimestamp(refresh_payload["exp"], tz=timezone.utc),
            )
        )

        access_token = create_jwt(
            secret=self.config.jwt_secret,
            subject=user_id,
            token_type="access",
            expires_delta=self.config.access_ttl,
            parent_jti=refresh_payload["jti"],
        )
        return {"access_token": access_token, "refresh_token": refresh_token}

    def rotate_refresh_token(self, refresh_token: str) -> dict[str, str]:
        payload = decode_jwt(refresh_token, secret=self.config.jwt_secret, expected_type="refresh")
        db_token = self.store.get_token(payload["jti"])
        if db_token is None:
            raise InvalidTokenError("Unknown refresh token")
        if db_token.revoked:
            self.store.revoke_descendants(db_token.jti, reason="refresh-token-reuse-detected")
            raise InvalidTokenError("Refresh token revoked")

        self.store.revoke_token(db_token.jti, reason="rotated")
        return self._issue_token_pair(int(payload["sub"]), parent_jti=db_token.jti)

    def revoke_session(self, refresh_token: str, *, reason: str) -> None:
        payload = decode_jwt(refresh_token, secret=self.config.jwt_secret, expected_type="refresh")
        self.store.revoke_token(payload["jti"], reason=reason)
        self.store.revoke_descendants(payload["jti"], reason=reason)

    def authenticate_access_token(self, access_token: str) -> User:
        payload = decode_jwt(access_token, secret=self.config.jwt_secret, expected_type="access")
        user = self.store.get_user_by_id(int(payload["sub"]))
        if not user or not user.is_active:
            raise InvalidTokenError("Inactive user")
        return user
