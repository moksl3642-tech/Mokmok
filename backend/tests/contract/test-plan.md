# API Contract Test Plan (OpenAPI Compliance)

## Mục tiêu
Đảm bảo API implementation khớp với đặc tả OpenAPI (request/response/schema/status code).

## Phạm vi kiểm thử

- Mỗi endpoint có test cho:
  - Request hợp lệ -> status code đúng.
  - Request sai schema -> status code lỗi đúng.
  - Response body đúng schema OpenAPI.
- Header bắt buộc (auth/content-type/correlation-id nếu có).
- Versioning và backward compatibility cho endpoint cũ.

## Cách triển khai gợi ý

- Dùng OpenAPI source of truth (`openapi.yaml`/`json`).
- Tự động sinh validator hoặc chạy tool contract test.
- Chặn merge nếu có endpoint lệch spec.

## Tiêu chí pass

- 100% endpoint trong scope release có contract test.
- Không có mismatch giữa runtime response và OpenAPI schema.
