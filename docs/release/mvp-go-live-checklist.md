# MVP Go-live Checklist - `v1.0.0-mvp`

**Ngày kiểm tra:** 2026-03-07  
**Release owner:** PM/Tech Lead

## Checklist bắt buộc trước Go-live

- [x] **Backup/restore đã diễn tập**
  - [x] Đã thực hiện backup dữ liệu trước phát hành.
  - [x] Đã chạy diễn tập restore trên môi trường kiểm thử.
  - [x] Đã xác nhận thời gian phục hồi nằm trong ngưỡng chấp nhận.

- [x] **Monitoring/alerting đã bật**
  - [x] Bật giám sát availability cho dịch vụ chính.
  - [x] Bật cảnh báo lỗi ứng dụng và tài nguyên hệ thống.
  - [x] Đã kiểm tra kênh nhận cảnh báo (email/chat/on-call).

- [x] **Runbook sự cố và on-call đã phân công**
  - [x] Runbook xử lý sự cố đã được rà soát và cập nhật.
  - [x] Danh sách on-call có đủ vai trò (app, infra, dữ liệu).
  - [x] Có cơ chế escalation khi sự cố vượt ngưỡng.

## Trạng thái tổng hợp

| Hạng mục | Trạng thái |
|---|---|
| Backup/restore drill | ✅ GREEN |
| Monitoring/alerting | ✅ GREEN |
| Runbook + On-call | ✅ GREEN |

**Kết luận go-live:** ✅ **ALL GREEN** — đủ điều kiện phát hành MVP.
