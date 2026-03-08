# SLI/SLO cho tính ổn định hệ thống

## 1) Phạm vi & nguyên tắc
- **Mục tiêu theo dõi:** dịch vụ API/Backend và các thành phần phụ trợ (DB, cache, queue).
- **Chu kỳ đánh giá:** rolling 28 ngày.
- **Đối tượng đo:** production traffic.
- **Error budget mặc định:** `100% - SLO`.

## 2) Danh mục SLI/SLO

| Nhóm | SLI | Định nghĩa | SLO mục tiêu | Cửa sổ đo | Mức cảnh báo |
|---|---|---|---|---|---|
| Availability | API Availability | Tỷ lệ request thành công (HTTP 2xx/3xx + business success) trên tổng request | **>= 99.90%** | 28 ngày | Warning khi < 99.95%, Critical khi < 99.90% |
| Error rate | API Error Rate | Tỷ lệ lỗi 5xx + timeout + exception chưa bắt được | **<= 0.10%** | 28 ngày | Warning khi > 0.08%, Critical khi > 0.10% |
| Latency P95 | API P95 Latency | p95 `http_request_duration_seconds` (không gồm healthcheck) | **<= 300ms** | 7 ngày & 28 ngày | Warning khi > 250ms, Critical khi > 300ms |
| Latency P99 | API P99 Latency | p99 `http_request_duration_seconds` (không gồm healthcheck) | **<= 800ms** | 7 ngày & 28 ngày | Warning khi > 700ms, Critical khi > 800ms |
| DB Health | DB Availability + Saturation | DB up, tỉ lệ timeout/kết nối lỗi, CPU/IO saturation | **Up >= 99.95%**, timeout <= 0.05% | 28 ngày | Warning khi timeout > 0.03%, Critical khi > 0.05% |
| Cache Hit Ratio | Cache Hit Ratio | `cache_hits / (cache_hits + cache_misses)` | **>= 92%** | 7 ngày & 28 ngày | Warning khi < 94%, Critical khi < 92% |
| Queue Lag | Queue Lag | Độ trễ message (enqueue -> consume) p95 | **<= 60s** | 7 ngày & 28 ngày | Warning khi > 45s, Critical khi > 60s |

## 3) Công thức đo (PromQL gợi ý)

### Availability
```promql
sum(rate(http_requests_total{status=~"2..|3..",route!="/healthz"}[5m]))
/
sum(rate(http_requests_total{route!="/healthz"}[5m]))
```

### Error Rate
```promql
sum(rate(http_requests_total{status=~"5..",route!="/healthz"}[5m]))
/
sum(rate(http_requests_total{route!="/healthz"}[5m]))
```

### Latency P95/P99
```promql
histogram_quantile(
  0.95,
  sum(rate(http_request_duration_seconds_bucket{route!="/healthz"}[5m])) by (le)
)
```

```promql
histogram_quantile(
  0.99,
  sum(rate(http_request_duration_seconds_bucket{route!="/healthz"}[5m])) by (le)
)
```

### DB timeout/error
```promql
sum(rate(db_request_errors_total[5m])) / sum(rate(db_requests_total[5m]))
```

### Cache Hit Ratio
```promql
sum(rate(cache_hits_total[5m]))
/
(sum(rate(cache_hits_total[5m])) + sum(rate(cache_misses_total[5m])))
```

### Queue Lag P95
```promql
histogram_quantile(
  0.95,
  sum(rate(queue_message_lag_seconds_bucket[5m])) by (le)
)
```

## 4) Chính sách hành động theo error budget
- **Burn rate < 1x:** vận hành bình thường.
- **Burn rate 1x - 2x:** hạn chế release rủi ro cao, tăng quan sát.
- **Burn rate > 2x:** đóng băng release tính năng, ưu tiên reliability fixes.
- **Burn rate > 4x kéo dài > 1h:** kích hoạt quy trình incident mức cao.

## 5) Quy ước báo cáo
- Báo cáo tuần dùng mẫu: `docs/ops/weekly-report-YYYY-WW.md`.
- Báo cáo cuối kỳ: `docs/ops/stability-report.md`.
- Mọi sự cố cần có hồ sơ tại `docs/ops/incidents/` và liên kết trong báo cáo tuần/cuối kỳ.
