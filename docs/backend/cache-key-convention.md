# Cache key convention & invalidation design

## 1) Key convention

Quy ước chung:

- Pattern: `<domain>:{<id>}[:<subdomain>][:<dimension>][:v<schema_version>]`
- Dùng chữ thường, phân tách bằng `:`.
- Mọi key có dữ liệu phụ thuộc cấu hình thuật toán phải gắn `algo:{algo_version}` để dễ invalidation theo version.
- Không encode dữ liệu lớn vào key; chỉ dùng định danh, timeframe, filter hash ngắn.

### Danh sách key chuẩn

#### Roadmap snapshot

- `shoe:{shoe_id}:roadmaps:algo:{algo_version}:v1`
  - Payload: snapshot roadmap tổng hợp theo shoe.
  - Kiểu: JSON nén (hoặc MessagePack).
- `session:{session_id}:roadmaps:algo:{algo_version}:v1`
  - Payload: snapshot roadmap theo session đang chạy.

#### Thống kê tổng hợp (aggregate stats)

- `session:{session_id}:stats:agg:{window}:algo:{algo_version}:v1`
  - Ví dụ `window`: `last_50`, `last_200`, `all`.
- `shoe:{shoe_id}:stats:agg:{window}:algo:{algo_version}:v1`

#### Forecast

- `session:{session_id}:forecast:{horizon}:algo:{algo_version}:v1`
  - Ví dụ `horizon`: `next_1`, `next_3`, `next_5`.
- `shoe:{shoe_id}:forecast:{horizon}:algo:{algo_version}:v1`

#### Metadata phục vụ invalidation nhanh

- `idx:session:{session_id}:cache-keys`
  - Redis Set chứa danh sách key liên quan session.
- `idx:shoe:{shoe_id}:cache-keys`
  - Redis Set chứa danh sách key liên quan shoe.
- `cfg:algorithm:active-version`
  - Lưu phiên bản cấu hình thuật toán đang active.

---

## 2) Caching cho payload đọc nhiều / tính toán nặng

Áp dụng cache-aside cho 3 nhóm payload:

1. Roadmap snapshot.
2. Aggregate stats.
3. Forecast.

Luồng đọc chuẩn:

1. Đọc Redis theo key convention.
2. Nếu hit: trả về ngay.
3. Nếu miss: tính toán từ source of truth (DB/event store), ghi cache (set + TTL), trả về response.
4. Ghi key vào index set `idx:*:cache-keys` để hỗ trợ invalidation theo entity.

Tối ưu thêm:

- Dùng `singleflight` (hoặc distributed lock ngắn) để tránh cache stampede khi miss hàng loạt.
- Optional warm-up sau deploy hoặc sau invalidation lớn cho các key nóng.

---

## 3) Invalidation theo event

### A. Event nhập hand mới (`hand.created`)

Khi phát sinh hand mới trong `session_id`, `shoe_id`:

- Xóa toàn bộ key thuộc session trong `idx:session:{session_id}:cache-keys`.
- Xóa toàn bộ key thuộc shoe trong `idx:shoe:{shoe_id}:cache-keys`.
- Giữ lại idempotency bằng event_id (tránh xử lý trùng).

Lý do: roadmap/stats/forecast đều phụ thuộc dữ liệu hand mới.

### B. Event sửa/xóa hand (`hand.updated`, `hand.deleted`)

- Invalidate tương tự `hand.created` (session + shoe scope).
- Nếu payload có dimension theo window/horizon, vẫn chọn invalidate toàn bộ entity scope để tránh thiếu sót dependency.

### C. Event cập nhật cấu hình thuật toán (`algorithm.config.updated`)

Chiến lược khuyến nghị: **versioned key + lazy cutover**

1. Tăng `algo_version` mới vào `cfg:algorithm:active-version`.
2. Request mới chỉ đọc/ghi key có `algo:{algo_version_moi}`.
3. Key cũ hết hạn tự nhiên theo TTL hoặc dọn nền (background cleanup).

Ưu điểm: tránh delete hàng loạt và giảm spike tải DB do thundering herd.

---

## 4) TTL & fallback khi Redis unavailable

## TTL đề xuất

- Roadmap snapshot: `TTL = 30s` (near-real-time).
- Aggregate stats: `TTL = 60s`.
- Forecast: `TTL = 45s`.
- Jitter ngẫu nhiên `±10%` để giảm đồng bộ hết hạn.

## Fallback strategy

Khi Redis lỗi/timeout:

1. **Read path**:
   - Bypass cache, đọc từ DB/service tính toán trực tiếp.
   - Ghi metric `cache_unavailable_total`.
2. **Write path (set cache)**:
   - Best-effort, không block response nếu set thất bại.
3. **Resilience**:
   - Timeout Redis ngắn (ví dụ 30–50ms nội bộ).
   - Circuit breaker mở khi lỗi vượt ngưỡng, tự phục hồi theo half-open probe.
4. **Optional local fallback cache**:
   - In-memory LRU TTL rất ngắn (5–10s) cho key nóng để giảm tải tức thời khi Redis mất kết nối.
   - Chỉ dùng cho dữ liệu không yêu cầu mạnh về real-time.

---

## 5) Tiêu chí hoàn tất (Definition of Done)

## Chỉ số bắt buộc

- Cache hit ratio:
  - Roadmap snapshot: `>= 85%`
  - Aggregate stats: `>= 80%`
  - Forecast: `>= 75%`
- P95 latency read endpoint giảm tối thiểu `30%` so với baseline chưa cache.

## SLA stale data

- Không có stale data vượt SLA:
  - Roadmap: tối đa `30s`.
  - Stats: tối đa `60s`.
  - Forecast: tối đa `45s`.
- 99.9% request phải tuân thủ SLA freshness.

## Kiểm thử/quan sát bắt buộc

- Unit test cho key builder + invalidation selector theo event type.
- Integration test cho flow cache miss/hit/invalidate/fallback Redis down.
- Dashboard gồm: hit ratio, miss ratio, invalidation lag, Redis error rate, stale-age histogram.
- Alert:
  - Hit ratio xuống dưới ngưỡng 15 phút liên tiếp.
  - Stale-age vượt SLA >0.1% request trong 5 phút.
