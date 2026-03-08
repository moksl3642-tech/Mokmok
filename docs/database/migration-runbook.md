# Migration Runbook

## 1) Mục tiêu
Chuẩn hóa quy trình migrate schema/data giữa các môi trường (dev/staging/prod) để:
- Giảm rủi ro downtime và lỗi dữ liệu.
- Đảm bảo khả năng rollback có kiểm soát.
- Có đầy đủ log/audit cho mỗi lần thực thi.

## 2) Phạm vi
- Áp dụng cho tất cả migration liên quan DB ứng dụng.
- Áp dụng cho cả thay đổi DDL và DML có tác động dữ liệu.

## 3) Vai trò & trách nhiệm
- **DB Owner**: duyệt kế hoạch migration, giám sát chỉ số sau triển khai.
- **On-call Engineer**: thực thi migration theo checklist, ghi execution log.
- **Reviewer**: kiểm tra script up/down, tính idempotent, lock/risk.

## 4) Tiêu chuẩn trước khi chạy (Pre-check)
- Migration phải có cặp script **up/down** (hoặc chiến lược rollback tương đương nếu down bất khả thi).
- Đã chạy thử trên staging và có kết quả rõ ràng.
- Ước lượng thời gian thực thi + lock impact.
- Có backup gần nhất (<= 24h) và đã xác nhận restore khả dụng.
- Có maintenance window (nếu cần) và kế hoạch truyền thông.

## 5) Quy ước migration
- Tên migration: `YYYYMMDDHHMM_<short_description>`.
- Mỗi migration mô tả:
  - Mục đích.
  - Tác động dữ liệu.
  - Backward compatibility.
  - Điều kiện rollback.

## 6) Quy trình migrate UP (staging/prod)
1. Khóa phiên triển khai (deployment lock) để tránh chạy song song.
2. Kiểm tra kết nối DB + quyền user migration.
3. Chạy dry-run (nếu công cụ hỗ trợ) hoặc `plan`.
4. Thực thi migration UP theo thứ tự phiên bản.
5. Ghi nhận:
   - version bắt đầu/kết thúc,
   - thời gian bắt đầu/kết thúc,
   - số migration thành công/thất bại.
6. Chạy kiểm tra sau migrate:
   - schema tồn tại đúng,
   - query smoke test,
   - metrics lỗi/độ trễ.
7. Cập nhật `migration-execution-log.md`.

## 7) Quy trình migrate DOWN (rollback)
1. Kích hoạt khi có tiêu chí rollback (SLO lỗi vượt ngưỡng, lỗi dữ liệu, không tương thích).
2. Dừng ghi mới hoặc bật chế độ hạn chế ghi (nếu cần).
3. Chạy migration DOWN theo phạm vi đã phát hành.
4. Kiểm tra tính nhất quán dữ liệu sau rollback.
5. Ghi log rollback vào `migration-execution-log.md`.
6. Mở lại traffic khi hệ thống ổn định.

## 8) Tiêu chí dừng khẩn cấp
- Migration vượt quá thời gian dự kiến > 2x.
- Lock chặn truy cập nghiệp vụ chính > ngưỡng chấp nhận.
- Tăng mạnh lỗi ứng dụng liên quan DB.

## 9) Checklist thực thi nhanh
- [ ] Có ticket/change request được duyệt.
- [ ] Backup mới nhất hợp lệ.
- [ ] Đã xác nhận kế hoạch rollback.
- [ ] Đã thông báo cửa sổ triển khai.
- [ ] Đã ghi execution log sau khi xong.

## 10) Liên kết tài liệu vận hành
- Nhật ký migration: `docs/database/migration-execution-log.md`
- Nhật ký backup: `docs/database/backup-log.md`
- Báo cáo DR drill: `docs/database/dr-drill-report.md`
## 1) Cấu trúc migration

- Thư mục gốc: `backend/migrations/`
- Tool sử dụng: SQL migration runner nội bộ (`backend/migrations/runner.py`) — tương đương Alembic cho luồng up/down.
- Nhóm migration:
  - `baseline/`: DDL nền tảng ban đầu.
  - `feature/`: thay đổi theo tính năng.
  - `hotfix/`: vá nóng khẩn cấp.
- Naming convention file:
  - up: `YYYYMMDDHHMMSS_<group>_<short_description>__up.sql`
  - down: `YYYYMMDDHHMMSS_<group>_<short_description>__down.sql`

## 2) Quy tắc apply

- `baseline` phải chạy trước `feature`, và `feature` trước `hotfix`.
- Bảng `schema_migrations` lưu lịch sử phiên bản đã apply.
- Mỗi migration bắt buộc có đủ cặp `__up.sql` và `__down.sql`.

## 3) Apply/Rollback ở local

### Local - DB trống

```bash
rm -f backend/local.db
python3 backend/migrations/runner.py upgrade head --db backend/local.db
python3 backend/db/seeds/run_seeds.py --db backend/local.db
python3 backend/migrations/runner.py downgrade base --db backend/local.db
```

### Local - DB có dữ liệu mẫu

```bash
rm -f backend/sample.db
python3 backend/migrations/runner.py upgrade head --db backend/sample.db
python3 backend/db/seeds/run_seeds.py --db backend/sample.db
python3 backend/migrations/runner.py downgrade -1 --db backend/sample.db
python3 backend/migrations/runner.py upgrade head --db backend/sample.db
python3 backend/migrations/runner.py downgrade base --db backend/sample.db
```

## 4) Staging workflow

1. Backup DB staging.
2. Apply migrations:

```bash
python3 backend/migrations/runner.py upgrade head --db <staging_db_path>
```

3. Apply seed nếu môi trường cần dữ liệu mặc định:

```bash
python3 backend/db/seeds/run_seeds.py --db <staging_db_path>
```

4. Smoke test các bảng `roles`, `algorithm_configs`, `educational_contents`.
5. Rollback khi cần:

```bash
python3 backend/migrations/runner.py downgrade -1 --db <staging_db_path>
# hoặc rollback toàn bộ
python3 backend/migrations/runner.py downgrade base --db <staging_db_path>
```

## 5) Production workflow

1. Freeze deploy + backup snapshot.
2. Chạy migration theo batch release:

```bash
python3 backend/migrations/runner.py upgrade head --db <production_db_path>
```

3. Xác nhận healthcheck + truy vấn sanity check.
4. Nếu lỗi, rollback revision mới nhất trước:

```bash
python3 backend/migrations/runner.py downgrade -1 --db <production_db_path>
```

## 6) Migration rủi ro cao & rollback path

- `20260307103000_hotfix_algorithm_key_unique` là migration rủi ro cao do:
  - normalize `algorithm_configs.key` về lowercase;
  - xóa bản ghi trùng key;
  - thêm unique index.
- Rollback path:
  - trước khi biến đổi, dữ liệu gốc được snapshot vào `algorithm_configs_backup_hotfix_20260307103000`;
  - khi rollback, index bị gỡ và dữ liệu gốc được restore từ snapshot.
