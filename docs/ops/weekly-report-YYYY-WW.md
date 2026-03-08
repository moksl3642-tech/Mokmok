# Weekly Stability Report - YYYY-WW

> Dùng file này làm mẫu cho từng tuần theo định dạng `weekly-report-<năm>-<tuần>.md`.

## 1) Tóm tắt tuần
- Thời gian theo dõi: `<YYYY-MM-DD>` đến `<YYYY-MM-DD>`
- Mức độ ổn định chung: `Đạt / Không đạt`
- Incident phát sinh: `<Số lượng>`
- Thay đổi hạ tầng/release đáng chú ý:
  - `<item 1>`
  - `<item 2>`

## 2) Số liệu SLI/SLO trong tuần

| Chỉ số | SLO | Kết quả tuần | Trạng thái |
|---|---:|---:|---|
| Availability | >= 99.90% | `<xx.xx%>` | `✅/⚠️/❌` |
| Error rate | <= 0.10% | `<xx.xx%>` | `✅/⚠️/❌` |
| P95 latency | <= 300ms | `<xxx ms>` | `✅/⚠️/❌` |
| P99 latency | <= 800ms | `<xxx ms>` | `✅/⚠️/❌` |
| DB health (timeout/error) | <= 0.05% | `<xx.xx%>` | `✅/⚠️/❌` |
| Cache hit ratio | >= 92% | `<xx.xx%>` | `✅/⚠️/❌` |
| Queue lag p95 | <= 60s | `<xx s>` | `✅/⚠️/❌` |

## 3) Burn-rate & Error Budget
- Error budget còn lại (28 ngày): `<xx.xx%>`
- Burn rate trung bình: `<x.xx>`
- Khuyến nghị vận hành tuần tới:
  - `<action 1>`
  - `<action 2>`

## 4) Incident trong tuần

| Mã incident | Mức độ | Khoảng thời gian | Ảnh hưởng | Trạng thái RCA |
|---|---|---|---|---|
| `<INC-YYYY-WW-01>` | `<SEV>` | `<start-end>` | `<dịch vụ bị ảnh hưởng>` | `Đã xong / Đang xử lý` |

## 5) Kế hoạch tuần kế tiếp
- [ ] `<Reliability task 1>`
- [ ] `<Reliability task 2>`
- [ ] `<Reliability task 3>`
