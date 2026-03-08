# Stability Report (Kỳ theo dõi 4 tuần)

## 1) Phạm vi
- Kỳ theo dõi: 2025-12-29 đến 2026-01-25 (4 tuần liên tục).
- Nguồn dữ liệu: dashboard + alert rules trong `ops/monitoring/`.
- Tài liệu đối chiếu SLO: `docs/ops/slo-sli.md`.

## 2) Tổng hợp kết quả theo SLO

| Chỉ số | SLO | Tuần 01 | Tuần 02 | Tuần 03 | Tuần 04 | Kết luận kỳ |
|---|---:|---:|---:|---:|---:|---|
| Availability | >= 99.90% | 99.93% | 99.95% | 99.91% | 99.96% | ✅ Đạt |
| Error rate | <= 0.10% | 0.07% | 0.05% | 0.08% | 0.04% | ✅ Đạt |
| P95 latency | <= 300ms | 271ms | 248ms | 287ms | 233ms | ✅ Đạt |
| P99 latency | <= 800ms | 754ms | 701ms | 782ms | 663ms | ✅ Đạt |
| DB health (timeout/error) | <= 0.05% | 0.04% | 0.03% | 0.05% | 0.03% | ✅ Đạt |
| Cache hit ratio | >= 92% | 92.8% | 93.6% | 92.4% | 94.2% | ✅ Đạt |
| Queue lag p95 | <= 60s | 49s | 42s | 57s | 39s | ✅ Đạt |

## 3) Đối chiếu với tiêu chí hoàn tất
- **Tiêu chí:** KPI/SLO đạt ngưỡng ổn định trong toàn bộ kỳ theo dõi.
- **Kết quả:** Tất cả SLO đều đạt trong cả 4 tuần; không có tuần nào vượt ngưỡng vi phạm.
- **Kết luận:** **Hoàn tất** theo tiêu chí đã đề ra.

## 4) Incident & RCA
- Tổng số incident: 2 (đều mức SEV-3, đã đóng).
- Hồ sơ chi tiết:
  - `docs/ops/incidents/INC-2026-01-01.md`
  - `docs/ops/incidents/INC-2026-03-01.md`

## 5) Hành động khắc phục / phòng ngừa tái diễn (CAPA)
1. Tối ưu index + query plan cho endpoint search nặng.
2. Bổ sung autoscaling queue consumer theo queue depth và queue lag.
3. Áp dụng cache warm-up khi deploy để giảm cold-start penalty.
4. Thiết lập kiểm thử tải định kỳ theo kịch bản giờ cao điểm.
5. Đưa burn-rate review vào checklist release hàng tuần.

## 6) Kiến nghị chu kỳ kế tiếp
- Nâng mục tiêu cache hit ratio từ 92% lên 93% sau khi baseline ổn định thêm 1 chu kỳ.
- Theo dõi thêm SLI theo tenant/region để phát hiện hotspot sớm.
