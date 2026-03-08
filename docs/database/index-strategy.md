# Database Index Strategy

Tài liệu này mô tả mapping **query -> index -> expected benefit** cho các truy vấn chính của hệ thống.

## 1) Timeline theo session

### Query pattern
```sql
SELECT id, hand_no, result, created_at
FROM app.hands
WHERE session_id = $1
ORDER BY created_at DESC
LIMIT 100;
```

### Index
- `idx_hands_session_created_at ON app.hands (session_id, created_at DESC)`

### Expected benefit
- Biến full scan thành index range scan theo `session_id`.
- Trả kết quả đã sắp xếp sẵn theo `created_at DESC`, giảm sort cost.

---

## 2) Pattern timeline theo session

### Query pattern
```sql
SELECT id, pattern_type, confidence, created_at
FROM app.patterns
WHERE session_id = $1
ORDER BY created_at DESC
LIMIT 100;
```

### Index
- `idx_patterns_session_created_at ON app.patterns (session_id, created_at DESC)`

### Expected benefit
- Tối ưu lọc + sắp xếp trên tập dữ liệu lớn của pattern events.

---

## 3) Shoes timeline theo session

### Query pattern
```sql
SELECT id, shoe_no, status, created_at
FROM app.shoes
WHERE session_id = $1
ORDER BY created_at DESC;
```

### Index
- `idx_shoes_session_created_at ON app.shoes (session_id, created_at DESC)`

### Expected benefit
- Tránh sequential scan khi truy vấn lịch sử shoe theo session.

---

## 4) Danh sách user active

### Query pattern
```sql
SELECT id, email, username
FROM auth.users
WHERE status = 'active'
  AND email = $1;
```

### Index
- `idx_users_active_email ON auth.users (email) WHERE status = 'active'`

### Expected benefit
- Partial index nhỏ hơn nhiều so với full index.
- Tăng hit-rate cho workload truy vấn user active.

---

## 5) Session active theo user

### Query pattern
```sql
SELECT id, started_at
FROM app.sessions
WHERE user_id = $1
  AND status = 'active'
ORDER BY started_at DESC
LIMIT 20;
```

### Index
- `idx_sessions_active_user_started ON app.sessions (user_id, started_at DESC) WHERE status = 'active'`

### Expected benefit
- Truy vấn active session gần như index-only range scan.
- Không cần sort ngoài.

---

## 6) Pattern active

### Query pattern
```sql
SELECT id, pattern_type, created_at
FROM app.patterns
WHERE session_id = $1
  AND status = 'active'
ORDER BY created_at DESC;
```

### Index
- `idx_patterns_active_session_created ON app.patterns (session_id, created_at DESC) WHERE status = 'active'`

### Expected benefit
- Hạn chế đọc dữ liệu `inactive/archived`, giảm I/O.

---

## 7) Filter JSONB user settings

### Query pattern
```sql
SELECT id, user_id, preferences
FROM app.user_settings
WHERE preferences @> '{"theme": "dark"}'::jsonb;
```

### Index
- `idx_user_settings_preferences_gin ON app.user_settings USING GIN (preferences jsonb_path_ops)`

### Expected benefit
- Giảm mạnh cost cho toán tử containment `@>` trên JSONB.

---

## 8) Filter JSONB algorithm config

### Query pattern
```sql
SELECT id, config_key, version
FROM system.algorithm_config
WHERE config @> '{"mode": "aggressive"}'::jsonb;
```

### Index
- `idx_algorithm_config_gin ON system.algorithm_config USING GIN (config jsonb_path_ops)`

### Expected benefit
- Tăng tốc truy vấn feature flags / mode lookup từ cấu hình JSON.

---

## 9) Filter JSONB audit metadata

### Query pattern
```sql
SELECT id, action, created_at
FROM system.audit_logs
WHERE metadata @> '{"ip": "10.0.0.1"}'::jsonb
ORDER BY created_at DESC;
```

### Index
- `idx_audit_logs_metadata_gin ON system.audit_logs USING GIN (metadata jsonb_path_ops)`

### Expected benefit
- Hỗ trợ lọc metadata linh hoạt mà vẫn giữ hiệu năng tốt khi volume log tăng.

---

## Tiêu chí xác nhận (EXPLAIN)

Sử dụng file `backend/db/explain-plans.sql` để chạy `EXPLAIN (ANALYZE, BUFFERS)` cho các query chính.

Kỳ vọng:
- Planner chọn `Index Scan`, `Bitmap Index Scan` hoặc `Index Only Scan` cho các pattern đã liệt kê.
- Không còn `Seq Scan` ngoài ý muốn trên các bảng lớn (`hands`, `patterns`, `audit_logs`).
- Nếu planner vẫn chọn `Seq Scan` với dữ liệu nhỏ, cần benchmark lại khi có dữ liệu production-like và cập nhật thống kê bằng `ANALYZE`.
