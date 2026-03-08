# Backend API Test Plan (Mokmok)

## 1) Mục tiêu
- Xác thực tính đúng đắn, bảo mật, hiệu năng và độ ổn định cho các API trọng yếu:
  - Auth
  - Nhập hand
  - Analysis
  - Roadmap
  - Admin
- Đặt chuẩn SLA để dùng làm pass/fail cho load test.

## 2) Phạm vi API trọng yếu

| Domain | Endpoint mẫu | Chức năng chính | Rủi ro |
|---|---|---|---|
| Auth | `POST /api/auth/login`, `POST /api/auth/refresh`, `POST /api/auth/logout` | Đăng nhập, refresh token, đăng xuất | Brute force, token leak, broken auth |
| Nhập hand | `POST /api/hands`, `GET /api/hands/:id` | Nhập lịch sử hand và xem chi tiết | Injection, dữ liệu sai định dạng |
| Analysis | `POST /api/analysis/run`, `GET /api/analysis/:id` | Chạy phân tích hand | Job timeout, lỗi xử lý dữ liệu lớn |
| Roadmap | `GET /api/roadmap`, `POST /api/roadmap/progress` | Trả lộ trình học và cập nhật tiến độ | IDOR, privilege bypass |
| Admin | `GET /api/admin/users`, `PATCH /api/admin/users/:id/role` | Quản trị user/role | Privilege escalation |

> Ghi chú: endpoint thực tế cần map lại theo OpenAPI/spec khi hệ thống backend khả dụng.

## 3) Loại kiểm thử
- Functional/API contract
- Security (OWASP API Top 10)
- Performance/Load
- Reliability (timeout/retry/idempotency)

## 4) Ma trận test chính theo domain

### 4.1 Auth
- Login thành công/thất bại (sai mật khẩu, tài khoản khóa, user không tồn tại).
- Refresh token: token hợp lệ/hết hạn/revoked.
- Logout: token bị invalidate sau logout.
- Rate-limit cho login/refresh.

### 4.2 Nhập hand
- Validate schema (field bắt buộc, enum, số âm, size payload).
- Idempotency khi gửi lại cùng request-id.
- Truy xuất hand theo quyền sở hữu (user A không đọc hand user B).

### 4.3 Analysis
- Chạy phân tích với input nhỏ/lớn/biên.
- Timeout và retry policy.
- Tính nhất quán trạng thái job: queued/running/succeeded/failed.

### 4.4 Roadmap
- Lấy roadmap theo role/user.
- Cập nhật tiến độ hợp lệ/không hợp lệ.
- Không cho phép user sửa roadmap của user khác.

### 4.5 Admin
- Chỉ admin truy cập được endpoint admin.
- Chặn hạ quyền/tăng quyền trái phép.
- Audit log cho thao tác nhạy cảm.

## 5) Dữ liệu test
- 3 role: `user`, `coach`, `admin`.
- 2 tenant giả lập (nếu có multi-tenant).
- Tập hand data: nhỏ (5 actions), vừa (50), lớn (500+).

## 6) SLA hiệu năng (ngưỡng pass/fail)

| API nhóm | P95 | P99 | Error rate | Throughput tối thiểu |
|---|---:|---:|---:|---:|
| Auth | <= 250ms | <= 500ms | < 1.0% | >= 150 req/s |
| Nhập hand | <= 400ms | <= 800ms | < 1.0% | >= 80 req/s |
| Analysis | <= 1200ms | <= 2500ms | < 2.0% | >= 30 req/s |
| Roadmap | <= 300ms | <= 700ms | < 1.0% | >= 100 req/s |
| Admin | <= 500ms | <= 1000ms | < 1.0% | >= 40 req/s |

## 7) Tiêu chí hoàn tất
- Không còn lỗ hổng mức Critical/High ở trạng thái Open.
- Tất cả kịch bản baseline + peak đạt SLA.
- Stress test có thể degrade có kiểm soát nhưng không gây crash toàn hệ thống.

## 8) Trạng thái hiện tại trong repo
- Chưa có source backend/service runtime và chưa có OpenAPI spec trong repository hiện tại.
- Vì vậy, kế hoạch này là baseline test plan để triển khai khi môi trường backend sẵn sàng.
