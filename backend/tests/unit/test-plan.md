# Unit Test Plan (Service/Engine)

## Mục tiêu
Đảm bảo business logic ở tầng `service/engine` hoạt động đúng, độc lập với DB và network.

## Phạm vi kiểm thử

- Validation đầu vào và xử lý giá trị biên.
- Branch logic theo role/trạng thái/feature flag.
- Error mapping (domain error -> API error).
- Idempotency, retry policy (nếu có).
- Deterministic behavior (không phụ thuộc thời gian/random nếu chưa mock).

## Cấu trúc case đề xuất

- `service_<domain>_happy_path`
- `service_<domain>_invalid_input`
- `service_<domain>_permission_denied`
- `engine_<flow>_state_transition`
- `engine_<flow>_error_propagation`

## Tiêu chí pass

- 100% test unit xanh.
- Coverage service layer quan trọng >= 85% (line + branch nếu tool hỗ trợ).
