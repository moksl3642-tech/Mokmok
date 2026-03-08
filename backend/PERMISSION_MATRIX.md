# Permission Matrix

| Endpoint | Anonymous | User | Admin |
|---|---|---|---|
| `POST /auth/login` | allow | allow | allow |
| `POST /auth/session/refresh` | allow with valid refresh token | allow | allow |
| `POST /auth/session/revoke` | allow with valid refresh token | allow | allow |
| `POST /hands/input` | deny | allow | allow |
| `GET /admin/users` | deny | deny | allow |
| `PATCH /admin/system/config` | deny | deny | allow + audit log |
| `GET /admin/audit-logs` | deny | deny | allow |
| `GET /permissions/matrix` | allow | allow | allow |

All admin endpoints (`/admin/*`) are protected by role guard `require_roles("admin")`.
