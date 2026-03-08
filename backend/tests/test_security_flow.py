from __future__ import annotations

from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.security.dependencies import container


client = TestClient(app)


def setup_function() -> None:
    container.store.users_by_id.clear()
    container.store.users_by_username.clear()
    container.store.tokens.clear()
    container.store.user_tokens.clear()
    container.store.audit_logs.clear()
    container.rate_limiter.requests.clear()
    app.router.startup()


def _login(username: str, password: str) -> dict[str, str]:
    response = client.post("/auth/login", json={"username": username, "password": password})
    assert response.status_code == 200
    return response.json()


def _headers(access_token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {access_token}"}


def test_password_hashing_and_login() -> None:
    stored_user = container.store.get_user_by_username("user")
    assert stored_user is not None
    assert stored_user.password_hash != "user123"

    ok = client.post("/auth/login", json={"username": "user", "password": "user123"})
    assert ok.status_code == 200
    bad = client.post("/auth/login", json={"username": "user", "password": "bad"})
    assert bad.status_code == 401


def test_jwt_rotation_and_revocation() -> None:
    tokens = _login("user", "user123")
    refresh_resp = client.post("/auth/session/refresh", json={"refresh_token": tokens["refresh_token"]})
    assert refresh_resp.status_code == 200
    new_tokens = refresh_resp.json()

    reuse_resp = client.post("/auth/session/refresh", json={"refresh_token": tokens["refresh_token"]})
    assert reuse_resp.status_code == 401

    revoke_resp = client.post("/auth/session/revoke", json={"refresh_token": new_tokens["refresh_token"]})
    assert revoke_resp.status_code == 200

    after_revoke = client.post("/auth/session/refresh", json={"refresh_token": new_tokens["refresh_token"]})
    assert after_revoke.status_code == 401


def test_rbac_allow_and_deny_on_admin_endpoints() -> None:
    user_tokens = _login("user", "user123")
    admin_tokens = _login("admin", "admin123")

    deny_users = client.get("/admin/users", headers=_headers(user_tokens["access_token"]))
    assert deny_users.status_code == 403

    allow_users = client.get("/admin/users", headers=_headers(admin_tokens["access_token"]))
    assert allow_users.status_code == 200
    assert "admin" in allow_users.json()["users"]

    deny_config = client.patch(
        "/admin/system/config",
        json={"maintenance_mode": True},
        headers=_headers(user_tokens["access_token"]),
    )
    assert deny_config.status_code == 403

    allow_config = client.patch(
        "/admin/system/config",
        json={"maintenance_mode": True},
        headers=_headers(admin_tokens["access_token"]),
    )
    assert allow_config.status_code == 200


def test_rate_limiting_sensitive_endpoints() -> None:
    for _ in range(5):
        response = client.post("/auth/login", json={"username": "user", "password": "bad"})
        assert response.status_code == 401

    blocked = client.post("/auth/login", json={"username": "user", "password": "user123"})
    assert blocked.status_code == 429


def test_hand_input_requires_auth_and_is_rate_limited() -> None:
    unauth = client.post("/hands/input", json={"value": "abc"})
    assert unauth.status_code == 401

    tokens = _login("user", "user123")
    for _ in range(10):
        ok = client.post(
            "/hands/input",
            json={"value": "abc"},
            headers=_headers(tokens["access_token"]),
        )
        assert ok.status_code == 200

    blocked = client.post(
        "/hands/input",
        json={"value": "abc"},
        headers=_headers(tokens["access_token"]),
    )
    assert blocked.status_code == 429


def test_audit_log_for_admin_config_change() -> None:
    admin_tokens = _login("admin", "admin123")

    patch_response = client.patch(
        "/admin/system/config",
        json={"maintenance_mode": True},
        headers=_headers(admin_tokens["access_token"]),
    )
    assert patch_response.status_code == 200

    logs_response = client.get("/admin/audit-logs", headers=_headers(admin_tokens["access_token"]))
    assert logs_response.status_code == 200
    logs = logs_response.json()["logs"]
    assert len(logs) == 1
    assert logs[0]["action"] == "system.config.update"
    assert logs[0]["target"] == "system.config"


def test_permission_matrix_visibility() -> None:
    response = client.get("/permissions/matrix")
    assert response.status_code == 200
    matrix = response.json()
    assert matrix["/admin/users"]["user"] == "deny"
    assert matrix["/admin/users"]["admin"] == "allow"
