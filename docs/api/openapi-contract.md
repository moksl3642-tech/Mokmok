# API OpenAPI Contract Baseline

## 1) API Versioning Standard

- Base path bắt buộc: **`/api/v1`**.
- Mọi endpoint public phải nằm dưới `/api/v1/{module}`.
- Không cho phép endpoint mới ở root path không version.

### Backward compatibility policy
1. **Minor-safe changes (không phá vỡ)**
   - Thêm field optional trong response.
   - Thêm endpoint mới.
   - Thêm enum value mới nếu client được khuyến nghị ignore unknown.
2. **Breaking changes (phá vỡ)**
   - Đổi tên/xóa field response đã public.
   - Đổi kiểu dữ liệu field.
   - Đổi semantic của status code chính.
   - Yêu cầu field mới ở request body mà không có default.
3. **Quy tắc phát hành**
   - Breaking change => tạo version mới (`/api/v2`).
   - Có ít nhất 1 chu kỳ deprecation trước khi remove endpoint của version cũ.
   - Trả header khuyến nghị deprecation:
     - `Deprecation: true`
     - `Sunset: <RFC-1123 date>`

## 2) Shared Pydantic Schemas (chuẩn đặt tên)

```python
class ErrorResponse(BaseModel):
    code: str
    message: str
    details: dict[str, Any] | None = None

class Paging(BaseModel):
    page: int = Field(ge=1)
    page_size: int = Field(ge=1, le=200)
    total: int = Field(ge=0)

class Meta(BaseModel):
    request_id: str
    timestamp: datetime
```

Tất cả response dạng list dùng cấu trúc:
```python
class ListResponse(BaseModel, Generic[T]):
    items: list[T]
    paging: Paging
    meta: Meta
```

## 3) Module contracts

> Ghi chú: tên schema dưới đây là canonical để đồng bộ trực tiếp với Pydantic models trong code.

## 3.1 Auth (`/api/v1/auth`)

### POST `/api/v1/auth/register`
- Request schema: `AuthRegisterRequest`
```python
class AuthRegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    display_name: str = Field(min_length=1, max_length=80)
```
- Response schema: `AuthRegisterResponse`
```python
class AuthRegisterResponse(BaseModel):
    user_id: UUID
    email: EmailStr
    status: Literal["active", "pending_verification"]
    meta: Meta
```

### POST `/api/v1/auth/login`
- Request: `AuthLoginRequest`
- Response: `AuthTokenResponse`
```python
class AuthLoginRequest(BaseModel):
    email: EmailStr
    password: str

class AuthTokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: Literal["bearer"] = "bearer"
    expires_in: int
    meta: Meta
```

### POST `/api/v1/auth/refresh`
- Request: `AuthRefreshRequest`
- Response: `AuthTokenResponse`

### POST `/api/v1/auth/logout`
- Request: `AuthLogoutRequest`
- Response: `AuthLogoutResponse`
```python
class AuthRefreshRequest(BaseModel):
    refresh_token: str

class AuthLogoutRequest(BaseModel):
    refresh_token: str

class AuthLogoutResponse(BaseModel):
    success: bool
    meta: Meta
```

## 3.2 Sessions (`/api/v1/sessions`)

### POST `/api/v1/sessions`
- Request: `SessionCreateRequest`
- Response: `SessionResponse`
```python
class SessionCreateRequest(BaseModel):
    roadmap_id: UUID | None = None
    title: str = Field(min_length=1, max_length=120)
    hand_ids: list[UUID] = Field(default_factory=list)

class SessionResponse(BaseModel):
    session_id: UUID
    user_id: UUID
    status: Literal["draft", "active", "closed"]
    started_at: datetime | None = None
    ended_at: datetime | None = None
    meta: Meta
```

### GET `/api/v1/sessions/{session_id}`
- Response: `SessionResponse`

### POST `/api/v1/sessions/{session_id}/close`
- Request: `SessionCloseRequest`
- Response: `SessionResponse`
```python
class SessionCloseRequest(BaseModel):
    reason: str | None = Field(default=None, max_length=255)
```

### GET `/api/v1/sessions`
- Query: `page`, `page_size`, `status`
- Response: `ListResponse[SessionSummary]`
```python
class SessionSummary(BaseModel):
    session_id: UUID
    title: str
    status: Literal["draft", "active", "closed"]
    started_at: datetime | None = None
    ended_at: datetime | None = None
```

## 3.3 Hands (`/api/v1/hands`)

### POST `/api/v1/hands`
- Request: `HandCreateRequest`
- Response: `HandResponse`
```python
class HandCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=150)
    content: dict[str, Any]
    difficulty: Literal["beginner", "intermediate", "advanced"]
    tags: list[str] = Field(default_factory=list, max_length=20)

class HandResponse(BaseModel):
    hand_id: UUID
    version: int
    title: str
    difficulty: Literal["beginner", "intermediate", "advanced"]
    tags: list[str]
    meta: Meta
```

### GET `/api/v1/hands/{hand_id}`
- Response: `HandResponse`

### GET `/api/v1/hands`
- Query: `difficulty`, `tag`, `page`, `page_size`
- Response: `ListResponse[HandSummary]`
```python
class HandSummary(BaseModel):
    hand_id: UUID
    title: str
    difficulty: Literal["beginner", "intermediate", "advanced"]
```

### PATCH `/api/v1/hands/{hand_id}`
- Request: `HandUpdateRequest`
- Response: `HandResponse`
```python
class HandUpdateRequest(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=150)
    content: dict[str, Any] | None = None
    difficulty: Literal["beginner", "intermediate", "advanced"] | None = None
    tags: list[str] | None = None
```

## 3.4 Analysis (`/api/v1/analysis`)

### POST `/api/v1/analysis/run`
- Request: `AnalysisRunRequest`
- Response: `AnalysisRunResponse`
```python
class AnalysisRunRequest(BaseModel):
    hand_id: UUID | None = None
    session_id: UUID | None = None
    mode: Literal["quick", "full"] = "quick"

class AnalysisRunResponse(BaseModel):
    analysis_id: UUID
    status: Literal["queued", "running", "done", "failed"]
    meta: Meta
```

### GET `/api/v1/analysis/{analysis_id}`
- Response: `AnalysisResultResponse`
```python
class AnalysisResultResponse(BaseModel):
    analysis_id: UUID
    status: Literal["queued", "running", "done", "failed"]
    score: float | None = None
    insights: list[str] = Field(default_factory=list)
    leaks: list[str] = Field(default_factory=list)
    meta: Meta
```

### GET `/api/v1/analysis`
- Query: `status`, `page`, `page_size`
- Response: `ListResponse[AnalysisSummary]`
```python
class AnalysisSummary(BaseModel):
    analysis_id: UUID
    status: Literal["queued", "running", "done", "failed"]
    created_at: datetime
```

## 3.5 Roadmaps (`/api/v1/roadmaps`)

### POST `/api/v1/roadmaps`
- Request: `RoadmapCreateRequest`
- Response: `RoadmapResponse`
```python
class RoadmapCreateRequest(BaseModel):
    objective: str = Field(min_length=3, max_length=300)
    target_weeks: int = Field(ge=1, le=104)

class RoadmapItem(BaseModel):
    item_id: UUID
    title: str
    status: Literal["todo", "doing", "done"]

class RoadmapResponse(BaseModel):
    roadmap_id: UUID
    objective: str
    status: Literal["active", "completed", "archived"]
    items: list[RoadmapItem] = Field(default_factory=list)
    meta: Meta
```

### GET `/api/v1/roadmaps/{roadmap_id}`
- Response: `RoadmapResponse`

### PATCH `/api/v1/roadmaps/{roadmap_id}/items/{item_id}`
- Request: `RoadmapProgressUpdateRequest`
- Response: `RoadmapItem`
```python
class RoadmapProgressUpdateRequest(BaseModel):
    status: Literal["todo", "doing", "done"]
    note: str | None = Field(default=None, max_length=500)
```

### GET `/api/v1/roadmaps`
- Query: `status`, `page`, `page_size`
- Response: `ListResponse[RoadmapSummary]`
```python
class RoadmapSummary(BaseModel):
    roadmap_id: UUID
    objective: str
    status: Literal["active", "completed", "archived"]
```

## 3.6 Admin (`/api/v1/admin`)

### GET `/api/v1/admin/users`
- Query: `status`, `role`, `page`, `page_size`
- Response: `ListResponse[AdminUserSummary]`
```python
class AdminUserSummary(BaseModel):
    user_id: UUID
    email: EmailStr
    status: Literal["active", "suspended", "deleted"]
    roles: list[str]
```

### POST `/api/v1/admin/users/{user_id}/suspend`
- Request: `AdminSuspendUserRequest`
- Response: `AdminSuspendUserResponse`
```python
class AdminSuspendUserRequest(BaseModel):
    reason: str = Field(min_length=3, max_length=255)

class AdminSuspendUserResponse(BaseModel):
    user_id: UUID
    status: Literal["suspended"]
    meta: Meta
```

### POST `/api/v1/admin/content/{hand_id}/moderate`
- Request: `ContentModerationRequest`
- Response: `ContentModerationResponse`
```python
class ContentModerationRequest(BaseModel):
    action: Literal["approve", "reject"]
    comment: str | None = Field(default=None, max_length=500)

class ContentModerationResponse(BaseModel):
    hand_id: UUID
    action: Literal["approve", "reject"]
    moderated_at: datetime
    meta: Meta
```

## 3.7 System (`/api/v1/system`)

### GET `/api/v1/system/healthz`
- Response: `HealthResponse`

### GET `/api/v1/system/readyz`
- Response: `ReadinessResponse`

### GET `/api/v1/system/version`
- Response: `VersionResponse`
```python
class HealthResponse(BaseModel):
    status: Literal["ok", "degraded"]
    checks: dict[str, str]
    meta: Meta

class ReadinessResponse(BaseModel):
    ready: bool
    dependencies: dict[str, Literal["up", "down"]]
    meta: Meta

class VersionResponse(BaseModel):
    service: str
    version: str
    api_version: Literal["v1"]
    commit_sha: str
    meta: Meta
```

## 4) Error contract (áp dụng toàn cục)
- HTTP 400/401/403/404/409/422/429/500 phải trả `ErrorResponse`.
- `code` là machine-readable stable key (ví dụ: `AUTH_INVALID_CREDENTIALS`).
- `message` ưu tiên user-facing message ngắn.
- `details` cho field-level validation/errors nội bộ.

## 5) Completion criteria (coverage)
- 100% endpoint trong các module `auth`, `sessions`, `hands`, `analysis`, `roadmaps`, `admin`, `system` có request/response contract.
- 100% schema tên gọi nhất quán với Pydantic model naming ở code.
- Mỗi endpoint đều thuộc `/api/v1` và tuân thủ backward compatibility policy bên trên.
