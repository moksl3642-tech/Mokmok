# Security Test Checklist

## 1) Auth Bypass

- [ ] Truy cập endpoint protected không token phải bị chặn (401/403).
- [ ] Token hết hạn/revoked phải bị từ chối.
- [ ] JWT signature/alg confusion bị chặn.
- [ ] Không thể giả mạo user id/tenant id qua payload.

## 2) Injection

- [ ] SQL Injection trên query/filter/search không thực thi payload độc hại.
- [ ] NoSQL/ORM injection được sanitize/parameterized.
- [ ] Command injection bị chặn ở mọi integration shell/system call.
- [ ] Template/serialization injection không thực thi code ngoài ý muốn.

## 3) Broken Access Control

- [ ] User thường không truy cập được resource admin.
- [ ] Kiểm tra IDOR: đổi `resource_id` không xem/sửa được dữ liệu người khác.
- [ ] Role escalation qua API bị chặn.
- [ ] Tenant isolation đúng trong môi trường multi-tenant.

## Bổ sung bắt buộc trong CI

- [ ] Chạy SAST/Dependency scan tối thiểu mỗi PR.
- [ ] Security regression test chạy cho endpoint nhạy cảm.
- [ ] Báo cáo security scan được lưu artifact.
