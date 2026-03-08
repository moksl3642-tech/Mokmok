# Weekly Ops Report - 2026-W07

## Tổng quan KPI tuần
- Availability: **99.97%** (đạt)
- Error rate: **0.22%** (đạt)
- P95/P99 latency: **382ms / 790ms** (đạt)
- Queue delay: **p95 18s** (đạt)
- DB health: pool **66%**, slow query p95 **90ms**, replication lag **0.7s** (đạt)
- Cache hit ratio: **89.0%** (đạt)

## Product KPI
- Retention D1/D7/D30: **34% / 20% / 11%** (đạt)
- Tỷ lệ Quick vs Detailed: **65% / 35%** (đạt)
- Tỷ lệ xem tab thống kê: **38%** (đạt)

## Incident trong tuần
- INC-2026-07-01 (SEV-3, 11 phút): cache miss tăng tại 1 nhóm endpoint thống kê.

### RCA
- TTL cache cho truy vấn thống kê được giảm quá thấp trong lần tối ưu trước.

### Hành động phòng ngừa tái diễn
- Khôi phục TTL chuẩn và áp dụng jitter TTL.
- Thêm regression check cho cache hit ratio trong pipeline hiệu năng.

## Trạng thái sự cố nghiêm trọng mở
- Không có.
