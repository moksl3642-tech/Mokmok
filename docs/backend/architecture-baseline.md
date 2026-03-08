# Backend Architecture Baseline (Mokmok)

## 1) Mục tiêu
Tài liệu này chuẩn hóa ranh giới module backend, ownership dữ liệu, và traceability từ yêu cầu nghiệp vụ sang code để làm baseline cho API `/api/v1`.

## 2) Bounded Context / Module Boundaries

### 2.1 `auth`
**Trách nhiệm chính**
- Đăng ký, đăng nhập, refresh token, logout.
- Quản lý danh tính người dùng và phân quyền role-based.

**Bao gồm**
- Password policy, lockout policy, JWT/OAuth2 token lifecycle.
- Xác thực đầu vào cho thông tin tài khoản.

**Không bao gồm**
- Không quản lý vòng đời session học tập (thuộc `sessions`).
- Không xử lý phân tích hand (thuộc `analysis`).

### 2.2 `sessions`
**Trách nhiệm chính**
- Vòng đời một training/study session.
- Theo dõi trạng thái session, tiến độ, và dữ liệu runtime liên quan session.

**Bao gồm**
- Tạo session, cập nhật trạng thái, đóng session.
- Liên kết session với user và roadmap.

**Không bao gồm**
- Không lưu trữ hand definitions chuẩn (thuộc `hands`).
- Không làm recommendation (thuộc `roadmaps`).

### 2.3 `hands`
**Trách nhiệm chính**
- CRUD dữ liệu hand (bài/tình huống tay bài), metadata, phân loại.
- Nguồn dữ liệu chuẩn cho session và analysis.

**Bao gồm**
- Validation cấu trúc hand, tags, difficulty.
- Quản lý phiên bản của hand content.

**Không bao gồm**
- Không tính scoring/insight phân tích (thuộc `analysis`).

### 2.4 `analysis`
**Trách nhiệm chính**
- Chạy pipeline phân tích hand/session và trả insight.
- Lưu kết quả phân tích và chỉ số hiệu suất.

**Bao gồm**
- Đánh giá quality score, leak detection, recommendation inputs.
- Quản lý trạng thái analysis jobs (nếu async).

**Không bao gồm**
- Không định nghĩa roadmap học tập (thuộc `roadmaps`).

### 2.5 `roadmaps`
**Trách nhiệm chính**
- Tạo và cập nhật roadmap học tập từ profile + analytics.
- Mapping objective -> milestone -> task.

**Bao gồm**
- Recommendation rules và trạng thái tiến trình roadmap.

**Không bao gồm**
- Không trực tiếp thực thi session runtime (thuộc `sessions`).

### 2.6 `admin`
**Trách nhiệm chính**
- Backoffice operations: quản trị user, content moderation, audit review.
- Cấu hình hệ thống ở mức vận hành nghiệp vụ.

**Bao gồm**
- Quản trị role, override giới hạn, duyệt nội dung.

**Không bao gồm**
- Không thay thế các API public module; chỉ gọi qua service contract nội bộ.

### 2.7 `system`
**Trách nhiệm chính**
- Health, readiness, metrics, feature flags, metadata phiên bản.
- Các endpoint phục vụ vận hành hệ thống.

**Bao gồm**
- `/healthz`, `/readyz`, `/metrics`, `/version`.

**Không bao gồm**
- Không xử lý nghiệp vụ domain.

## 3) Chuẩn kiến trúc code
- **Router layer**: chỉ nhận/validate request và map response model.
- **Service layer**: chứa business rules; không phụ thuộc transport.
- **Repository layer**: truy cập DB, không chứa business logic.
- **Schema layer (Pydantic)**: chuẩn hóa request/response contract.

Mỗi endpoint bắt buộc map theo pipeline:
`router -> service -> repository -> table`.

## 4) Ownership matrix: Endpoint và bảng dữ liệu

| Module | Endpoint prefix | Bảng sở hữu chính | Mô tả trách nhiệm |
|---|---|---|---|
| auth | `/api/v1/auth/*` | `users`, `credentials`, `roles`, `user_roles`, `refresh_tokens` | Danh tính, xác thực, phân quyền |
| sessions | `/api/v1/sessions/*` | `sessions`, `session_events`, `session_participants` | Vòng đời session và sự kiện runtime |
| hands | `/api/v1/hands/*` | `hands`, `hand_versions`, `hand_tags`, `hand_tag_map` | Kho hand và metadata |
| analysis | `/api/v1/analysis/*` | `analysis_jobs`, `analysis_results`, `analysis_metrics` | Phân tích và insight |
| roadmaps | `/api/v1/roadmaps/*` | `roadmaps`, `roadmap_items`, `roadmap_progress` | Lộ trình học tập và tiến độ |
| admin | `/api/v1/admin/*` | `audit_logs`, `content_moderations`, `system_configs` | Vận hành backoffice, kiểm soát |
| system | `/api/v1/system/*` | `feature_flags`, `system_events` | Health, metrics, feature & metadata |

## 5) Traceability mapping (requirement -> router -> service -> table)

| Requirement ID | Mô tả nghiệp vụ | Router (FastAPI) | Service | Bảng dữ liệu chính |
|---|---|---|---|---|
| REQ-AUTH-001 | Người dùng đăng nhập bằng email/password | `app.api.v1.auth.router:POST /auth/login` | `AuthService.login` | `users`, `credentials`, `refresh_tokens` |
| REQ-AUTH-002 | Refresh access token | `app.api.v1.auth.router:POST /auth/refresh` | `AuthService.refresh_token` | `refresh_tokens` |
| REQ-SESS-001 | Tạo session học mới | `app.api.v1.sessions.router:POST /sessions` | `SessionService.create_session` | `sessions` |
| REQ-SESS-002 | Đóng session | `app.api.v1.sessions.router:POST /sessions/{session_id}/close` | `SessionService.close_session` | `sessions`, `session_events` |
| REQ-HAND-001 | Tạo hand mới | `app.api.v1.hands.router:POST /hands` | `HandService.create_hand` | `hands`, `hand_versions` |
| REQ-HAND-002 | Liệt kê hand theo filter | `app.api.v1.hands.router:GET /hands` | `HandService.list_hands` | `hands`, `hand_tag_map` |
| REQ-ANL-001 | Chạy phân tích cho hand/session | `app.api.v1.analysis.router:POST /analysis/run` | `AnalysisService.run_analysis` | `analysis_jobs`, `analysis_results` |
| REQ-ANL-002 | Lấy kết quả phân tích | `app.api.v1.analysis.router:GET /analysis/{analysis_id}` | `AnalysisService.get_analysis` | `analysis_results`, `analysis_metrics` |
| REQ-RDM-001 | Tạo roadmap từ mục tiêu học | `app.api.v1.roadmaps.router:POST /roadmaps` | `RoadmapService.create_roadmap` | `roadmaps`, `roadmap_items` |
| REQ-RDM-002 | Cập nhật tiến độ roadmap item | `app.api.v1.roadmaps.router:PATCH /roadmaps/{roadmap_id}/items/{item_id}` | `RoadmapService.update_progress` | `roadmap_progress` |
| REQ-ADM-001 | Admin khóa user | `app.api.v1.admin.router:POST /admin/users/{user_id}/suspend` | `AdminService.suspend_user` | `users`, `audit_logs` |
| REQ-SYS-001 | Kiểm tra health | `app.api.v1.system.router:GET /system/healthz` | `SystemService.healthz` | `system_events` |

## 6) Definition of Done (DoD)
Được xem là hoàn tất baseline khi thỏa tất cả điều kiện:
1. 100% endpoint public có owner module (`auth/sessions/hands/analysis/roadmaps/admin/system`).
2. 100% bảng nghiệp vụ có owner module duy nhất.
3. Mỗi endpoint có mô tả trách nhiệm và map tới service xử lý.
4. Mỗi requirement quan trọng có traceability row (requirement -> router -> service -> table).
5. Contract request/response được định nghĩa trong `docs/api/openapi-contract.md` và dùng cùng tên schema Pydantic.
6. Tất cả endpoint tuân thủ prefix version `/api/v1`.

## 7) Governance
- Khi thêm endpoint mới: bắt buộc cập nhật cả 3 nơi:
  1) Router code.
  2) Pydantic schema.
  3) `docs/api/openapi-contract.md` + mapping traceability.
- Không merge PR nếu endpoint/bảng mới chưa có owner module rõ ràng.
