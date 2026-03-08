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
# SLO / SLI và Error Budget (tháng)

## Phạm vi
Áp dụng cho toàn bộ luồng production: **API -> service -> DB/Redis/worker**.

## SLI định nghĩa

1. **Availability SLI**  
   - Tử số: số request thành công (`2xx`, `3xx`, và `4xx` không do hệ thống)  
   - Mẫu số: tổng request

2. **Latency SLI (p95)**  
   - p95 latency của request API theo `http_request_duration_seconds_bucket`

3. **Error Rate SLI**  
   - Tỷ lệ `5xx` trên tổng request

4. **Queue Freshness SLI**  
   - p95 queue lag theo `queue_consumer_lag_seconds`

5. **Cache Efficiency SLI**  
   - `cache_hit_ratio = hit / (hit + miss)`

## SLO mục tiêu

- **Availability**: >= `99.9%` theo cửa sổ rolling 30 ngày.
- **Latency p95**: <= `800ms` cho >= `99%` số cửa sổ 5 phút / tháng.
- **Latency p99**: <= `1.5s` cho >= `99%` số cửa sổ 5 phút / tháng.
- **Error rate (5xx)**: <= `1%` trung bình 30 ngày.
- **Queue lag p95**: <= `60s`.
- **DB pool usage**: <= `90%` sustained.
- **Cache hit ratio**: >= `70%`.

## Error budget theo tháng

### 1) Availability budget
- SLO: `99.9%`
- Error budget: `0.1%` downtime/error tương đương.
- Với 30 ngày (~43,200 phút), budget downtime tối đa: **43.2 phút/tháng**.

### 2) Error-rate budget
- Mục tiêu `5xx <= 1%`.
- Nếu vượt ngưỡng liên tục > 2 ngày hoặc burn-rate > 2x trong 1 giờ: đóng băng release không khẩn cấp.

## Burn-rate và cảnh báo

- **Fast burn (critical)**: error rate > `3%` trong `10m`.
- **Slow burn (warning)**: error rate > `1.5%` trong `1h`.
- **Latency critical**: p99 > `1.5s` trong `10m`.
- **Queue warning**: p95 lag > `60s` trong `15m`.

## Chính sách vận hành khi tiêu hao budget

- Burn-rate > 2x: tạm dừng tính năng mới, ưu tiên reliability.
- Burn-rate > 4x hoặc budget còn < 25%: kích hoạt incident process và on-call escalation.
- Budget cạn: freeze release (trừ hotfix), tổ chức postmortem bắt buộc.
