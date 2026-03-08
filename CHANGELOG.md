# Changelog

Tất cả thay đổi quan trọng của dự án sẽ được ghi nhận tại đây.

Định dạng dựa trên [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) và phiên bản tuân theo [Semantic Versioning](https://semver.org/).

## [1.0.0-mvp] - 2026-03-08

### Added
- Hoàn tất tài liệu phát hành MVP, gồm release notes, checklist go-live, UAT sign-off và bằng chứng deploy.
- Chuẩn hóa quy trình phát hành cho staging và production với các bước backup, migration, rollback, monitoring, alerting.

### Changed
- Bổ sung tiêu chí hoàn tất release MVP để đảm bảo có đủ tag phát hành, release notes, UAT sign-off và deploy logs.

### Security
- Bổ sung xác minh quyền truy cập secret/deployment trước go-live và quy trình phản ứng sự cố sau phát hành.

