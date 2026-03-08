# Performance Test Plan (Critical Scenarios)

## Mục tiêu
Đo hiệu năng cho các kịch bản trọng yếu và thiết lập ngưỡng regression.

## Kịch bản trọng yếu

- Đăng nhập/xác thực người dùng.
- Luồng đọc dữ liệu chính (top endpoints).
- Luồng ghi dữ liệu có transaction.
- Tác vụ nền quan trọng (nếu có queue/worker).

## Chỉ số theo dõi

- P50/P95/P99 latency.
- Throughput (RPS/TPS).
- Error rate.
- DB query time và lock wait.

## Ngưỡng gợi ý

- P95 latency endpoint đọc chính <= 300ms.
- P95 latency endpoint ghi chính <= 500ms.
- Error rate < 1% dưới tải chuẩn.

## Tiêu chí pass

- Không vượt ngưỡng latency/error đã thống nhất.
- Không có regression > 10% so với baseline gần nhất.
