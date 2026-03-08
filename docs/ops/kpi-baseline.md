# KPI Baseline Vận hành cốt lõi (MVP)

## 1) Mục tiêu vận hành (Core Reliability KPI)

| Nhóm KPI | Định nghĩa | Cách đo | Ngưỡng mục tiêu MVP | Cảnh báo |
|---|---|---|---|---|
| Availability | Tỷ lệ uptime dịch vụ khách hàng + admin | `1 - (downtime / total_time)` theo tuần | >= 99.90% | Warning < 99.90%, Critical < 99.50% |
| Error rate | Tỷ lệ request lỗi (HTTP 5xx + timeout) | `errors / total_requests` theo 5 phút và theo ngày | <= 0.50% | Warning > 0.50% (10m), Critical > 1.00% (5m) |
| P95 latency | Độ trễ phân vị 95 cho API chính | Histogram quantile theo endpoint | <= 450ms | Warning > 450ms (10m), Critical > 700ms (5m) |
| P99 latency | Độ trễ phân vị 99 cho API chính | Histogram quantile theo endpoint | <= 900ms | Warning > 900ms (10m), Critical > 1400ms (5m) |
| Queue delay | Độ trễ hàng đợi tác vụ async | `queue_oldest_message_age_seconds` | <= 30s | Warning > 30s (10m), Critical > 90s (5m) |
| DB health | Sức khỏe DB (kết nối, slow query, replication lag) | Pool usage, slow query p95, lag | Pool usage < 80%, slow p95 < 120ms, lag < 2s | Warning khi vượt ngưỡng 10m, Critical khi vượt 5m mức cao |
| Cache hit ratio | Tỷ lệ cache hit ở lớp đọc nhiều | `cache_hits / (hits + misses)` | >= 85% | Warning < 85% (15m), Critical < 75% (10m) |

## 2) Product KPI theo dõi sau MVP

| Product KPI | Định nghĩa | Mục tiêu MVP |
|---|---|---|
| Retention D1 | Tỷ lệ người dùng quay lại sau 1 ngày | >= 30% |
| Retention D7 | Tỷ lệ người dùng quay lại sau 7 ngày | >= 18% |
| Retention D30 | Tỷ lệ người dùng quay lại sau 30 ngày | >= 10% |
| Tỷ lệ sử dụng Quick vs Detailed | Tỷ trọng phiên sử dụng chế độ Quick / Detailed | Quick 60–75%, Detailed 25–40% |
| Tỷ lệ xem tab thống kê | Tỷ lệ người dùng active mở tab thống kê ít nhất 1 lần/tuần | >= 35% |

## 3) Chu kỳ đánh giá

- KPI vận hành: theo **5 phút** (real-time alert), tổng hợp **ngày/tuần**.
- Product KPI: theo **ngày**, chốt báo cáo **tuần**.
- Tiêu chí hoàn tất giai đoạn ổn định: tất cả KPI giữ trong ngưỡng mục tiêu liên tục trong tối thiểu **3 tuần liên tiếp**, không còn incident nghiêm trọng mở.
