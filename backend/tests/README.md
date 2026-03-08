# Backend Test Strategy & Quality Gate

Tài liệu này triển khai 7 yêu cầu kiểm thử:

1. Unit test cho service/engine tại `backend/tests/unit/`.
2. Integration test cho repository + migration + transaction tại `backend/tests/integration/`.
3. API contract test đối chiếu OpenAPI tại `backend/tests/contract/`.
4. Performance test cho kịch bản trọng yếu tại `backend/tests/performance/`.
5. Security test checklist tại `backend/tests/security/`.
6. Đặt gate trong CI: tất cả test pass và coverage tối thiểu >= 85% cho service layer quan trọng.
7. Tiêu chí hoàn tất: không còn fail test trên main branch, báo cáo test được lưu theo release.

## Cấu trúc thư mục

- `unit/test-plan.md`
- `integration/test-plan.md`
- `contract/test-plan.md`
- `performance/test-plan.md`
- `security/checklist.md`

## Quy ước báo cáo

CI tạo các artifact theo từng lần chạy:

- `backend-test-report-*`:
  - Unit: `backend/reports/unit/`
  - Integration: `backend/reports/integration/`
  - Contract: `backend/reports/contract/`
  - Performance: `backend/reports/performance/`
  - Security: `backend/reports/security/`

Khi tạo release, workflow sẽ đính kèm test report để lưu vết theo release.
