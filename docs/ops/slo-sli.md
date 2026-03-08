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
