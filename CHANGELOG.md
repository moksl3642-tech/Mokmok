# Changelog

Tất cả thay đổi đáng chú ý của dự án **Mokmok** sẽ được ghi lại trong tài liệu này.

Định dạng dựa trên [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) và tuân thủ [Semantic Versioning (SemVer)](https://semver.org/lang/vi/).

## [Unreleased]

### Planned
- Chưa có thay đổi được phát hành.

## [1.0.0-mvp] - 2026-03-07

### Phạm vi MVP (in-scope)
- Hoàn thiện nền tảng cơ sở cho luồng khách hàng (frontend).
- Hoàn thiện backend quản trị cho vận hành ban đầu.
- Hoàn thiện logic nghiệp vụ lõi ở backend.
- Chốt thiết kế cơ sở dữ liệu cho giai đoạn MVP.

### Ngoài phạm vi MVP (out-of-scope)
- Tối ưu hiệu năng nâng cao theo quy mô lớn.
- Tích hợp mở rộng với hệ thống bên thứ ba chưa bắt buộc.
- Báo cáo chuyên sâu và dashboard phân tích nâng cao.

### Added
- Thiết lập baseline tài liệu release cho phiên bản MVP.
- Bổ sung UAT sign-off với danh sách kịch bản đã pass và known issues.
- Bổ sung checklist go-live trạng thái “all green” trước phát hành.

### Known Issues (accepted for MVP)
- Một số hạng mục tối ưu UX mức độ thấp được defer sang post-MVP.
- Chưa triển khai cảnh báo thông minh theo ngữ cảnh nâng cao.

---

## Quy ước phiên bản
- `MAJOR`: thay đổi không tương thích ngược.
- `MINOR`: bổ sung tính năng tương thích ngược.
- `PATCH`: sửa lỗi tương thích ngược.
- Hậu tố tiền phát hành (ví dụ `-mvp`) dùng cho mốc phát hành theo phạm vi đặc biệt.
