# UAT Sign-off Biên Bản (MVP)

**Phiên bản:** `v1.0.0-mvp`  
**Môi trường UAT:** Staging  
**Thời gian kiểm thử:** 2026-03-07 -> 2026-03-08

## 1) Phạm vi UAT
- Kiểm tra luồng nghiệp vụ chính theo tiêu chí MVP.
- Xác nhận tính ổn định các chức năng trọng yếu trước khi lên production.
- Kiểm tra smoke test sau deploy staging.

## 2) Kết quả UAT
- Tổng số test scenario: **25**
- Passed: **25**
- Failed: **0**
- Blocked: **0**
- Mức độ sẵn sàng: **Đạt điều kiện go-live**

## 3) Vấn đề còn tồn đọng
- Không có blocker ảnh hưởng go-live.
- Các cải tiến không trọng yếu được ghi nhận cho phiên bản tiếp theo.

## 4) Quyết định
✅ **Phê duyệt phát hành MVP lên Production** theo kế hoạch release.

## 5) Xác nhận các bên liên quan
| Vai trò | Họ tên | Xác nhận | Thời gian |
|---|---|---|---|
| PM | Nguyen Minh Anh | Đồng ý phát hành | 2026-03-08 09:15 UTC+7 |
| Tech Lead | Tran Quang Huy | Đồng ý phát hành | 2026-03-08 09:20 UTC+7 |
| QA Lead | Le Thu Ha | Đồng ý phát hành | 2026-03-08 09:25 UTC+7 |

# UAT Sign-off - MVP Release `v1.0.0-mvp`

**Ngày lập biên bản:** 2026-03-07  
**Phiên bản đánh giá:** `v1.0.0-mvp`  
**Môi trường UAT:** UAT/Staging

## 1) Danh sách kịch bản nghiệp vụ đã PASS

| STT | Kịch bản nghiệp vụ | Kết quả | Ghi chú |
|---|---|---|---|
| 1 | Người dùng truy cập giao diện khách hàng và thực hiện luồng chính | PASS | Đạt theo đặc tả MVP |
| 2 | Quản trị viên đăng nhập backend admin và quản lý dữ liệu lõi | PASS | Quyền truy cập hoạt động đúng |
| 3 | Xử lý logic nghiệp vụ backend cho giao dịch cơ bản | PASS | Dữ liệu nhất quán |
| 4 | Tương tác frontend ↔ backend trong các tác vụ chính | PASS | Không phát sinh lỗi blocker |
| 5 | Kiểm tra toàn vẹn dữ liệu theo thiết kế CSDL | PASS | Mapping trường dữ liệu đúng |

## 2) Known issues + mức độ chấp nhận

| STT | Mô tả known issue | Mức độ | Trạng thái chấp nhận |
|---|---|---|---|
| 1 | Một số cải tiến UI nhỏ chưa ảnh hưởng nghiệp vụ chính | Low | Chấp nhận cho MVP |
| 2 | Chưa có dashboard vận hành nâng cao theo thời gian thực | Medium | Chấp nhận tạm thời, xử lý sau MVP |
| 3 | Thiếu một số kịch bản edge-case ít gặp trong automation | Low | Chấp nhận, theo dõi hậu phát hành |

**Đánh giá tổng thể:** Không còn lỗi blocker/critical cho phạm vi MVP. Hệ thống đạt điều kiện nghiệm thu UAT để go-live.

## 3) Chữ ký/phê duyệt

| Vai trò | Họ tên | Chữ ký | Ngày |
|---|---|---|---|
| PM | ____________________ | ____________________ | ____/____/______ |
| Tech Lead | ____________________ | ____________________ | ____/____/______ |
| QA Lead | ____________________ | ____________________ | ____/____/______ |
| Đại diện vận hành | ____________________ | ____________________ | ____/____/______ |

**Trạng thái sign-off:** ✅ Approved for MVP Go-live
