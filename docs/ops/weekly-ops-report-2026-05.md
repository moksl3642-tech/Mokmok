# Weekly Ops Report - 2026-W05

## Tổng quan KPI tuần
- Availability: **99.93%** (đạt)
- Error rate: **0.34%** (đạt)
- P95/P99 latency: **420ms / 870ms** (đạt)
- Queue delay: **p95 24s** (đạt)
- DB health: pool **72%**, slow query p95 **102ms**, replication lag **1.1s** (đạt)
- Cache hit ratio: **86.7%** (đạt)

## Product KPI
- Retention D1/D7/D30: **32% / 19% / 11%** (đạt)
- Tỷ lệ Quick vs Detailed: **68% / 32%** (đạt)
- Tỷ lệ xem tab thống kê: **36%** (đạt)

## Incident trong tuần
- INC-2026-05-01 (SEV-2, 18 phút): worker xử lý batch chậm do queue partition mất cân bằng.

### RCA
- Thiếu cơ chế autoscale theo queue depth.
- Một partition nhận tải đột biến từ import đồng thời.

### Hành động phòng ngừa tái diễn
- Thêm rule scale worker theo `queue_oldest_message_age_seconds`.
- Bổ sung cảnh báo sớm queue delay > 30s.
- Chuẩn hóa giới hạn tốc độ import theo tenant.

## Trạng thái sự cố nghiêm trọng mở
- Không có.
