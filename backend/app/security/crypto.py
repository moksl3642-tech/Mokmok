from __future__ import annotations

import base64
import hashlib
import hmac
import json
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import uuid4


class InvalidTokenError(ValueError):
    pass


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def hash_password(password: str, *, salt: bytes | None = None) -> str:
    salt = salt or secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 310_000)
    return f"pbkdf2_sha256${_b64url_encode(salt)}${_b64url_encode(digest)}"


def verify_password(password: str, encoded_hash: str) -> bool:
    algo, salt_b64, digest_b64 = encoded_hash.split("$", maxsplit=2)
    if algo != "pbkdf2_sha256":
        return False
    salt = _b64url_decode(salt_b64)
    expected = _b64url_decode(digest_b64)
    calculated = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 310_000)
    return hmac.compare_digest(expected, calculated)


def create_jwt(
    *,
    secret: str,
    subject: int,
    token_type: str,
    expires_delta: timedelta,
    jti: str | None = None,
    parent_jti: str | None = None,
) -> str:
    now = datetime.now(timezone.utc)
    payload: dict[str, Any] = {
        "sub": str(subject),
        "iat": int(now.timestamp()),
        "exp": int((now + expires_delta).timestamp()),
        "type": token_type,
        "jti": jti or str(uuid4()),
    }
    if parent_jti:
        payload["parent_jti"] = parent_jti
    header = {"alg": "HS256", "typ": "JWT"}
    encoded_header = _b64url_encode(json.dumps(header, separators=(",", ":")).encode("utf-8"))
    encoded_payload = _b64url_encode(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
    signing_input = f"{encoded_header}.{encoded_payload}".encode("ascii")
    signature = hmac.new(secret.encode("utf-8"), signing_input, hashlib.sha256).digest()
    return f"{encoded_header}.{encoded_payload}.{_b64url_encode(signature)}"


def decode_jwt(token: str, *, secret: str, expected_type: str | None = None) -> dict[str, Any]:
    try:
        encoded_header, encoded_payload, encoded_signature = token.split(".")
    except ValueError as exc:
        raise InvalidTokenError("Malformed token") from exc
    signing_input = f"{encoded_header}.{encoded_payload}".encode("ascii")
    actual_signature = _b64url_decode(encoded_signature)
    expected_signature = hmac.new(secret.encode("utf-8"), signing_input, hashlib.sha256).digest()
    if not hmac.compare_digest(actual_signature, expected_signature):
        raise InvalidTokenError("Invalid token signature")

    payload = json.loads(_b64url_decode(encoded_payload))
    now_epoch = int(datetime.now(timezone.utc).timestamp())
    if payload.get("exp", 0) < now_epoch:
        raise InvalidTokenError("Expired token")
    if expected_type and payload.get("type") != expected_type:
        raise InvalidTokenError("Invalid token type")
    return payload
