# Integration Test Plan (Repository + Migration + Transaction)

## Mục tiêu
Xác nhận repository làm việc đúng với schema thật, migration ổn định, transaction an toàn.

## Phạm vi kiểm thử

1. **Migration**
   - Apply migration từ đầu trên DB rỗng.
   - Rollback/re-apply (nếu hệ thống hỗ trợ down migration).
   - Smoke query sau migration.

2. **Repository CRUD**
   - Create/Read/Update/Delete đầy đủ field.
   - Unique constraint, foreign key constraint.
   - Soft delete/hard delete theo thiết kế.

3. **Transaction**
   - Commit thành công khi mọi thao tác hợp lệ.
   - Rollback toàn bộ khi có lỗi giữa chừng.
   - Concurrent transaction (lost update, deadlock handling).

## Dữ liệu test

- Sử dụng seed tối thiểu, deterministic.
- Mỗi test cô lập dữ liệu theo transaction hoặc schema riêng.

## Tiêu chí pass

- 100% integration test xanh.
- Không có migration lỗi trên môi trường CI clean.
