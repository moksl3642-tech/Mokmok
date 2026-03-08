# Migration Runbook

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
