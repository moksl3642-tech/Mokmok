# Performance & Security Test Plan

## 1) Mục tiêu

Đảm bảo các API trọng yếu đạt:

- SLA hiệu năng đã công bố (độ trễ P95/P99, throughput, error rate).
- Không còn lỗ hổng bảo mật mức **Critical/High** ở trạng thái mở.
- Cơ chế authN/authZ, rate limiting, input validation hoạt động đúng cho API và admin panel.

## 2) Phạm vi API trọng yếu

| Nhóm | Endpoint đại diện | Mức ưu tiên |
|---|---|---|
| Nhập hand | `POST /api/hands/import`, `POST /api/hands/validate` | P0 |
| Thống kê | `GET /api/stats/overview`, `GET /api/stats/detail` | P0 |
| Roadmap | `GET /api/roadmap`, `POST /api/roadmap/items` | P1 |
| Forecast | `GET /api/forecast`, `POST /api/forecast/recompute` | P1 |
| Auth/Admin | `POST /api/auth/login`, `POST /api/auth/refresh`, `GET /api/admin/users`, `PATCH /api/admin/users/:id/role` | P0 |

## 3) Môi trường & dữ liệu kiểm thử

- Môi trường: **staging** (cấu hình hạ tầng tương đương production về CPU/RAM/database cache policy).
- Dataset gần thực tế:
  - 1.2M records hand lịch sử.
  - 85k user accounts (bao gồm role user/analyst/admin).
  - 180k entries thống kê tổng hợp.
  - 12 tháng roadmap + forecast snapshots.
- Dữ liệu nhạy cảm dùng bản synthetic/masked.
- Seed dữ liệu cố định theo version để tái lập kết quả.

## 4) Kế hoạch performance testing

### 4.1 Workload profile

| Giai đoạn | Mục tiêu | VU đồng thời | Ramp-up | Thời lượng |
|---|---|---:|---:|---:|
| Baseline | Hiệu năng chuẩn vận hành thường ngày | 50 | 10 phút | 30 phút |
| Peak | Giờ cao điểm | 200 | 15 phút | 45 phút |
| Stress | Tìm ngưỡng suy giảm | 200 → 500 | 20 phút | 40 phút |
| Soak | Độ ổn định dài hạn | 150 | 15 phút | 8 giờ |

> Tỷ trọng traffic mô phỏng: Nhập hand 25%, thống kê 30%, roadmap 15%, forecast 10%, auth/admin 20%.

### 4.2 SLA mục tiêu

| API group | P95 latency | P99 latency | Throughput | Error rate |
|---|---:|---:|---:|---:|
| Nhập hand | ≤ 450ms | ≤ 900ms | ≥ 120 req/s | < 0.5% |
| Thống kê | ≤ 300ms | ≤ 700ms | ≥ 220 req/s | < 0.3% |
| Roadmap | ≤ 350ms | ≤ 800ms | ≥ 140 req/s | < 0.5% |
| Forecast | ≤ 500ms | ≤ 1000ms | ≥ 90 req/s | < 0.8% |
| Auth/Admin | ≤ 250ms | ≤ 600ms | ≥ 180 req/s | < 0.2% |

### 4.3 Công cụ và quan sát

- Load tool: k6/Gatling (kịch bản theo nhóm endpoint).
- Observability: APM traces, Prometheus metrics, DB slow query log.
- Thu thập:
  - Latency percentiles (P50/P95/P99).
  - Throughput theo endpoint.
  - Error breakdown (4xx/5xx/timeout).
  - Tài nguyên: CPU, RAM, DB connection pool, queue depth.

### 4.4 Tiêu chí pass/fail

- Pass khi **mọi API P0** đạt SLA trong baseline + peak + soak.
- Stress dùng để tìm ngưỡng; không bắt buộc pass tuyệt đối, nhưng phải có ngưỡng degrade rõ ràng và recovery thành công.
- Fail khi:
  - Error rate vượt ngưỡng SLA quá 5 phút liên tục.
  - P99 vượt SLA > 20% trong 3 lần chạy liên tiếp.

## 5) Kế hoạch penetration testing

### 5.1 Phạm vi kiểm thử bảo mật

- API public và API admin panel.
- Luồng đăng nhập, refresh token, revoke session.
- Phân quyền theo role (user/analyst/admin).
- Rate limiting và lockout.
- Input validation (body/query/path/header/upload).

### 5.2 Danh mục kiểm tra (OWASP Top 10)

1. Broken Access Control (IDOR, privilege escalation).
2. Cryptographic Failures (token/signature/secret handling).
3. Injection (SQL/NoSQL/command/template injection).
4. Insecure Design (business logic abuse).
5. Security Misconfiguration (CORS, headers, debug mode).
6. Vulnerable/Outdated Components.
7. Identification & Authentication Failures.
8. Software & Data Integrity Failures.
9. Security Logging & Monitoring Failures.
10. SSRF (nếu có endpoint gọi ra ngoài).

### 5.3 Phương pháp

- Kết hợp SAST + DAST + manual test case.
- Account matrix để kiểm thử authZ chéo role.
- Fuzzing input có kiểm soát cho endpoint nhập dữ liệu.
- Kiểm tra rate limit brute-force và password spraying.
- Thu thập evidence (request/response, log correlation ID, ảnh màn hình admin panel khi cần).

## 6) Remediation & Retest workflow

1. Ghi nhận lỗ hổng: severity, impact, bước tái hiện, bằng chứng.
2. Triage với dev owner + security owner, gán deadline:
   - Critical: 24h
   - High: 3 ngày
   - Medium: 10 ngày
   - Low: backlog
3. Khắc phục và mở PR có test case regression.
4. Retest độc lập bởi QA/security.
5. Cập nhật trạng thái:
   - **Closed**: đã fix và retest pass.
   - **Accepted risk**: có phê duyệt chính thức (kèm thời hạn review lại).

## 7) Tiêu chí hoàn tất chiến dịch

- Không còn lỗ hổng **Critical/High** ở trạng thái mở.
- SLA hiệu năng đạt ngưỡng đã công bố ở baseline/peak/soak.
- Báo cáo hoàn tất:
  - `docs/testing/load-test-report.md`
  - `docs/testing/pentest-report.md`
