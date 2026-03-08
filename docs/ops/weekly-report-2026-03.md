# Weekly Stability Report - 2026-03

## 1) Tóm tắt tuần
- Thời gian theo dõi: 2026-01-12 đến 2026-01-18
- Mức độ ổn định chung: Đạt
- Incident phát sinh: 1
- Thay đổi đáng chú ý: tăng replica cho queue consumer.

## 2) Số liệu SLI/SLO trong tuần

| Chỉ số | SLO | Kết quả tuần | Trạng thái |
|---|---:|---:|---|
| Availability | >= 99.90% | 99.91% | ✅ |
| Error rate | <= 0.10% | 0.08% | ✅ |
| P95 latency | <= 300ms | 287ms | ✅ |
| P99 latency | <= 800ms | 782ms | ✅ |
| DB health (timeout/error) | <= 0.05% | 0.05% | ✅ |
| Cache hit ratio | >= 92% | 92.4% | ✅ |
| Queue lag p95 | <= 60s | 57s | ✅ |

## 3) Burn-rate & Error Budget
- Error budget còn lại (28 ngày): 81.6%
- Burn rate trung bình: 0.94
- Khuyến nghị: thêm autoscaling rule theo queue depth.

## 4) Incident trong tuần
| Mã incident | Mức độ | Khoảng thời gian | Ảnh hưởng | Trạng thái RCA |
|---|---|---|---|---|
| INC-2026-03-01 | SEV-3 | 2026-01-16 21:20-21:55 | tăng queue lag | Đã xong |
