# Backup Log

## 1) Chính sách backup định kỳ
- **Full backup**: mỗi ngày lúc 00:30 UTC.
- **Incremental backup**: mỗi 6 giờ (06:30, 12:30, 18:30 UTC).
- **Retention**:
  - Daily full: 14 ngày.
  - Incremental: 7 ngày.
  - Weekly archive: 8 tuần.
- **Mã hóa**: AES-256 at-rest, TLS in-transit.
- **Vị trí lưu**: object storage đa AZ + bản sao vùng DR.

## 2) Trạng thái lịch chạy
- Cron/Scheduler: `enabled`
- Last verification: `2026-03-03 00:45 UTC`
- Alerting: gửi cảnh báo khi backup thất bại hoặc checksum mismatch.

## 3) Nhật ký thực thi backup

| Date (UTC) | Environment | Backup Type | Artifact ID | Size | Checksum | Result | Duration | Verified by |
|---|---|---|---|---|---|---|---|---|
| 2026-03-03 00:30 | prod | full | bkp-prod-20260303-full | 82 GB | sha256:9ab1...f6e2 | success | 14m20s | backup.bot |
| 2026-03-03 06:30 | prod | incremental | bkp-prod-20260303-inc-0630 | 6.8 GB | sha256:11fc...2ad9 | success | 3m42s | backup.bot |
| 2026-03-03 00:30 | staging | full | bkp-stg-20260303-full | 19 GB | sha256:3a71...bc10 | success | 5m31s | backup.bot |

## 4) Mẫu log

| Date (UTC) | Environment | Backup Type | Artifact ID | Size | Checksum | Result | Duration | Verified by |
|---|---|---|---|---|---|---|---|---|
| YYYY-MM-DD HH:mm | prod/staging | full/incremental | ... | ... | ... | success/failed | ... | ... |
