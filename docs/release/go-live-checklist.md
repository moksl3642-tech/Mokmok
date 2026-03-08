# Go-Live Checklist (MVP)

**Phiên bản:** `v1.0.0-mvp`  
**Ngày:** 2026-03-08  
**Owner phát hành:** Release Manager

## 1) Backup
- [ ] Backup database production thành công (full backup + verify restore metadata).
- [ ] Snapshot cấu hình hệ thống (env, config map, secrets metadata) trước deploy.
- [ ] Lưu vị trí backup (bucket/path) và retention policy.

## 2) Rollback
- [ ] Xác nhận artifact của bản ổn định trước đó còn khả dụng.
- [ ] Chuẩn bị kịch bản rollback one-command/one-playbook.
- [ ] Xác nhận người chịu trách nhiệm rollback (on-call engineer).
- [ ] Mô phỏng rollback trên staging trong vòng 7 ngày gần nhất.

## 3) Migrations
- [ ] Chạy migration dry-run trên staging và không có lỗi.
- [ ] Ước tính thời gian migration + lock impact được chấp thuận.
- [ ] Có script rollback migration (nếu khả thi) hoặc kế hoạch data fix.
- [ ] Xác nhận backup vừa tạo trước khi chạy migration production.

## 4) Monitoring
- [ ] Dashboard production đã cập nhật metric mới của MVP.
- [ ] Theo dõi các chỉ số chính: error rate, p95 latency, CPU, memory, DB connections.
- [ ] Thiết lập log correlation-id để truy vết lỗi sau release.

## 5) Alerting
- [ ] Alert HTTP 5xx > ngưỡng đã bật và gửi đúng kênh on-call.
- [ ] Alert latency p95 vượt ngưỡng đã bật.
- [ ] Alert DB connection pool saturation đã bật.
- [ ] Alert downtime healthcheck đã bật.

## 6) Go/No-Go
- [ ] PM xác nhận phạm vi release.
- [ ] Tech Lead xác nhận readiness kỹ thuật.
- [ ] QA xác nhận pass UAT và smoke test.
- [ ] Chốt quyết định **GO** trước cửa sổ phát hành.

