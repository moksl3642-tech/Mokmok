# Báo cáo tổng kết ổn định sau MVP

## 1) Phạm vi đánh giá
- Giai đoạn theo dõi ổn định: **4 tuần** (2026-W05 đến 2026-W08).
- Nguồn dữ liệu: dashboard KPI tại `ops/monitoring/dashboard-kpi.json`, rule cảnh báo tại `ops/monitoring/alerts-kpi.yaml`, và báo cáo tuần trong `docs/ops/`.

## 2) Đối chiếu KPI thực tế với mục tiêu MVP

| KPI | Mục tiêu MVP | Trung bình 4 tuần | Kết luận |
|---|---:|---:|---|
| Availability | >= 99.90% | 99.96% | Đạt |
| Error rate | <= 0.50% | 0.26% | Đạt |
| P95 latency | <= 450ms | 391ms | Đạt |
| P99 latency | <= 900ms | 808ms | Đạt |
| Queue delay | <= 30s | 19.25s | Đạt |
| DB pool usage | < 80% | 67.75% | Đạt |
| DB slow query p95 | < 120ms | 93.25ms | Đạt |
| DB replication lag | < 2s | 0.83s | Đạt |
| Cache hit ratio | >= 85% | 88.30% | Đạt |
| Retention D1 | >= 30% | 33.5% | Đạt |
| Retention D7 | >= 18% | 19.5% | Đạt |
| Retention D30 | >= 10% | 11.25% | Đạt |
| Quick/Detailed | 60–75% / 25–40% | 65.75% / 34.25% | Đạt |
| Tỷ lệ xem tab thống kê | >= 35% | 37.5% | Đạt |

## 3) Tình hình sự cố & RCA
- Tổng incident ghi nhận: **3** (1 SEV-2, 2 SEV-3).
- Không có incident SEV-1.
- Tất cả incident đã đóng, có RCA và hành động phòng ngừa cụ thể trong báo cáo tuần.

### Các nhóm nguyên nhân chính
1. Điều phối tài nguyên worker/queue chưa tối ưu khi tải tăng đột biến.
2. Cấu hình cache chưa ổn định sau thay đổi hiệu năng.

### Hành động phòng ngừa đã hoàn tất
- Áp dụng autoscaling worker dựa trên queue delay.
- Bổ sung alert sớm cho queue delay, cache hit ratio, latency.
- Cập nhật release checklist (pre-warm cache + kiểm tra migration lock).

## 4) Kết luận theo tiêu chí hoàn tất
- KPI duy trì trong ngưỡng mục tiêu liên tục trong chu kỳ theo dõi 4 tuần.
- Không còn sự cố nghiêm trọng mở.

**Kết luận:** Giai đoạn ổn định sau MVP đạt yêu cầu hoàn tất.
