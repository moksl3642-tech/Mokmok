# Weekly Stability Report - 2026-01

## 1) Tóm tắt tuần
- Thời gian theo dõi: 2025-12-29 đến 2026-01-04
- Mức độ ổn định chung: Đạt
- Incident phát sinh: 1
- Thay đổi đáng chú ý: rollout cache key normalization.

## 2) Số liệu SLI/SLO trong tuần

| Chỉ số | SLO | Kết quả tuần | Trạng thái |
|---|---:|---:|---|
| Availability | >= 99.90% | 99.93% | ✅ |
| Error rate | <= 0.10% | 0.07% | ✅ |
| P95 latency | <= 300ms | 271ms | ✅ |
| P99 latency | <= 800ms | 754ms | ✅ |
| DB health (timeout/error) | <= 0.05% | 0.04% | ✅ |
| Cache hit ratio | >= 92% | 92.8% | ✅ |
| Queue lag p95 | <= 60s | 49s | ✅ |

## 3) Burn-rate & Error Budget
- Error budget còn lại (28 ngày): 83.1%
- Burn rate trung bình: 0.86
- Khuyến nghị: theo dõi queue consumer khi traffic tăng giờ cao điểm.

## 4) Incident trong tuần
| Mã incident | Mức độ | Khoảng thời gian | Ảnh hưởng | Trạng thái RCA |
|---|---|---|---|---|
| INC-2026-01-01 | SEV-3 | 2026-01-03 10:05-10:33 | tăng latency endpoint search | Đã xong |
