# Runbook xử lý sự cố (Observability/SLO)

## 1. Mục tiêu
Khôi phục dịch vụ nhanh nhất, giảm impact người dùng, bảo toàn error budget.

## 2. Kích hoạt incident
Kích hoạt khi có 1 trong các alert:
- `HighErrorRate`
- `HighLatencyP99`
- `DBPoolSaturation`
- `QueueLagTooHigh`

## 3. Quy trình 15 phút đầu

1. **Triage**
   - Mở dashboard `Mokmok Service Reliability Dashboard`.
   - Xác định service bị ảnh hưởng.
2. **Containment**
   - Rollback release gần nhất (nếu có liên quan).
   - Bật rate limit / circuit breaker cho dependency lỗi.
3. **Diagnosis nhanh theo tín hiệu**
   - Error rate tăng + latency tăng: kiểm tra DB pool saturation.
   - Queue lag tăng: scale worker, kiểm tra downstream.
   - Cache hit ratio giảm: kiểm tra TTL/eviction, warm cache.
4. **Communication**
   - Cập nhật status page + thông báo stakeholder mỗi 15 phút.

## 4. Chẩn đoán chi tiết theo loại sự cố

### A) HighErrorRate
- Kiểm tra top route 5xx từ metrics `http_requests_total{status=~"5.."}`.
- Correlate trace theo `trace_id` trong log JSON.
- Xác nhận dependency đang timeout/retry storm.

### B) HighLatencyP95/P99
- Check spans DB/Redis trong trace waterfall.
- Tìm slow query và connection leak.
- Giảm tải bằng autoscale hoặc degrade non-critical features.

### C) QueueLagTooHigh
- Check worker throughput (`worker_jobs_total`).
- Kiểm tra dead-letter queue.
- Scale consumers hoặc giảm producer rate tạm thời.

### D) DBPoolSaturation
- Xác minh số kết nối in-use/max.
- Kill query chạy dài bất thường.
- Tăng connection pool tạm thời nếu DB còn headroom.

## 5. Điều kiện kết thúc incident
- Error rate về < 1% liên tục 30 phút.
- p95/p99 latency quay về ngưỡng SLO liên tục 30 phút.
- Queue lag về < 60s p95.
- Có timeline sự cố + owner cho action items.

## 6. Hậu kiểm (Postmortem)
- Hoàn thành trong 48h.
- Bao gồm: root cause, blast radius, MTTD/MTTR, bài học, preventive actions.
