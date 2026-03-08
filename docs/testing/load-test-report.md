# Load Test Report (Baseline / Peak / Stress)

## 1) Mục tiêu
Đo latency (P95/P99), throughput và error rate cho API trọng yếu theo 3 mức tải:
- Baseline
- Peak
- Stress

## 2) Môi trường & phương pháp
- Trạng thái repo hiện tại: **không có service backend chạy được**, không có endpoint thật để bắn tải.
- Vì vậy **chưa thể thực thi load test end-to-end** trong lần chạy này.
- SLA pass/fail áp dụng theo `backend-test-plan.md`.

## 3) Kết quả thực thi

| Mức tải | P95 | P99 | Throughput | Error rate | Kết luận |
|---|---:|---:|---:|---:|---|
| Baseline | N/A | N/A | N/A | N/A | ⚠️ Blocked (không có backend runtime) |
| Peak | N/A | N/A | N/A | N/A | ⚠️ Blocked (không có backend runtime) |
| Stress | N/A | N/A | N/A | N/A | ⚠️ Blocked (không có backend runtime) |

## 4) Ngưỡng pass/fail

| Chỉ số | Pass | Fail |
|---|---|---|
| P95, P99 | <= SLA của từng nhóm API | > SLA |
| Throughput | >= SLA của từng nhóm API | < SLA |
| Error rate | < SLA của từng nhóm API | >= SLA |

## 5) Kết luận hiện tại
- Không thể xác nhận pass/fail hiệu năng do thiếu môi trường backend thực thi.
- Cần bổ sung:
  1. URL service/staging.
  2. Bộ credential test.
  3. Danh sách endpoint thực tế + test data seed.

## 6) Khuyến nghị chạy lại
- Chạy theo thứ tự baseline → peak → stress.
- Mỗi mức tải tối thiểu 15 phút warm + 30 phút steady-state.
- Thu thập thêm CPU/RAM/DB metrics để correlation với latency.
