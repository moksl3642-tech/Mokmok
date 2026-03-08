# Weekly Ops Report - 2026-W06

## Tổng quan KPI tuần
- Availability: **99.95%** (đạt)
- Error rate: **0.29%** (đạt)
- P95/P99 latency: **398ms / 812ms** (đạt)
- Queue delay: **p95 20s** (đạt)
- DB health: pool **69%**, slow query p95 **95ms**, replication lag **0.9s** (đạt)
- Cache hit ratio: **88.1%** (đạt)

## Product KPI
- Retention D1/D7/D30: **33% / 19% / 11%** (đạt)
- Tỷ lệ Quick vs Detailed: **66% / 34%** (đạt)
- Tỷ lệ xem tab thống kê: **37%** (đạt)

## Incident trong tuần
- Không có incident từ SEV-2 trở lên.
- Sự kiện nhỏ: spike latency 7 phút sau deploy, tự phục hồi nhờ rollback canary.

### Hành động phòng ngừa tái diễn
- Bổ sung pre-warm cache sau deploy.
- Thêm checklist kiểm tra migration lock trước release.

## Trạng thái sự cố nghiêm trọng mở
- Không có.
