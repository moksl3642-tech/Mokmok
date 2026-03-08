# Weekly Stability Report - 2026-04

## 1) Tóm tắt tuần
- Thời gian theo dõi: 2026-01-19 đến 2026-01-25
- Mức độ ổn định chung: Đạt
- Incident phát sinh: 0
- Thay đổi đáng chú ý: triển khai warm-up cache khi deploy.

## 2) Số liệu SLI/SLO trong tuần

| Chỉ số | SLO | Kết quả tuần | Trạng thái |
|---|---:|---:|---|
| Availability | >= 99.90% | 99.96% | ✅ |
| Error rate | <= 0.10% | 0.04% | ✅ |
| P95 latency | <= 300ms | 233ms | ✅ |
| P99 latency | <= 800ms | 663ms | ✅ |
| DB health (timeout/error) | <= 0.05% | 0.03% | ✅ |
| Cache hit ratio | >= 92% | 94.2% | ✅ |
| Queue lag p95 | <= 60s | 39s | ✅ |

## 3) Burn-rate & Error Budget
- Error budget còn lại (28 ngày): 90.1%
- Burn rate trung bình: 0.66
- Khuyến nghị: giữ tần suất chaos test hàng tháng.
