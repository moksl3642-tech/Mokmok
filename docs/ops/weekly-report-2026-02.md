# Weekly Stability Report - 2026-02

## 1) Tóm tắt tuần
- Thời gian theo dõi: 2026-01-05 đến 2026-01-11
- Mức độ ổn định chung: Đạt
- Incident phát sinh: 0
- Thay đổi đáng chú ý: tối ưu index DB cho bảng giao dịch.

## 2) Số liệu SLI/SLO trong tuần

| Chỉ số | SLO | Kết quả tuần | Trạng thái |
|---|---:|---:|---|
| Availability | >= 99.90% | 99.95% | ✅ |
| Error rate | <= 0.10% | 0.05% | ✅ |
| P95 latency | <= 300ms | 248ms | ✅ |
| P99 latency | <= 800ms | 701ms | ✅ |
| DB health (timeout/error) | <= 0.05% | 0.03% | ✅ |
| Cache hit ratio | >= 92% | 93.6% | ✅ |
| Queue lag p95 | <= 60s | 42s | ✅ |

## 3) Burn-rate & Error Budget
- Error budget còn lại (28 ngày): 88.4%
- Burn rate trung bình: 0.73
- Khuyến nghị: tiếp tục tuning pool kết nối DB.
