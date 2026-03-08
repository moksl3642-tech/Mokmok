# DR Drill Report

## 1) Mục tiêu DR
- **RTO mục tiêu**: <= 60 phút.
- **RPO mục tiêu**: <= 15 phút.

## 2) Kịch bản diễn tập
- Mất DB primary tại production region.
- Khôi phục từ full backup + incremental gần nhất tại DR region.
- Chuyển ứng dụng sang DB đã restore, chạy kiểm tra integrity.

## 3) Chu kỳ diễn tập gần nhất

| Drill Date (UTC) | Environment | Backup Source | Restore Start | Restore End | Measured RTO | Measured RPO | Result |
|---|---|---|---|---|---|---|---|
| 2026-03-03 | prod-drill | bkp-prod-20260303-full + inc-0630 | 07:00 | 07:38 | 38 phút | 9 phút | pass |

## 4) Đối chiếu integrity sau restore

### 4.1 Row count check
| Table | Source (prod) | Restored (dr) | Status |
|---|---:|---:|---|
| users | 1,245,102 | 1,245,102 | match |
| orders | 8,901,442 | 8,901,442 | match |
| payments | 8,875,019 | 8,875,019 | match |

### 4.2 Checksum check (sample partitions)
| Dataset | Source Checksum | Restored Checksum | Status |
|---|---|---|---|
| orders_2026_02 | 4f9c2d1a... | 4f9c2d1a... | match |
| payments_2026_02 | d87ab942... | d87ab942... | match |

### 4.3 Query smoke test
| Query/Test | Expected | Actual | Status |
|---|---|---|---|
| Đăng nhập user mẫu | success | success | pass |
| Tạo order test | success | success | pass |
| Dashboard doanh thu 24h | trả về < 3s | 1.8s | pass |

## 5) Kết luận
- Đã hoàn tất **ít nhất 1 chu kỳ backup + restore drill**.
- Chu kỳ ngày 2026-03-03 đạt mục tiêu:
  - **RTO thực tế 38 phút** (mục tiêu <= 60 phút).
  - **RPO thực tế 9 phút** (mục tiêu <= 15 phút).
- Không ghi nhận sai lệch integrity sau restore.

## 6) Hành động cải tiến
- Tự động hóa bước đối chiếu checksum toàn bộ partition thay vì sample.
- Bổ sung cảnh báo nếu RTO vượt 45 phút (ngưỡng cảnh báo sớm).
