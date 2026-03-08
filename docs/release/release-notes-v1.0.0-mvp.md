# Release Notes - v1.0.0-mvp

**Release tag:** `v1.0.0-mvp`  
**Ngày phát hành dự kiến:** 2026-03-08  
**Môi trường:** Staging -> Production  

## 1) Tóm tắt
Phiên bản MVP tập trung đưa hệ thống vào vận hành thực tế với bộ tài liệu phát hành đầy đủ, quy trình go-live chuẩn hóa, và bằng chứng kiểm thử/chấp thuận triển khai.

## 2) Phạm vi bản phát hành
- Hoàn tất bộ tài liệu release cấp MVP.
- Xác nhận checklist go-live trước production.
- Chốt biên bản UAT với đầy đủ chữ ký PM/Tech Lead/QA.
- Lưu trữ log deploy staging và production phục vụ audit.

## 3) Thành phần bàn giao
- `CHANGELOG.md`
- `docs/release/go-live-checklist.md`
- `docs/release/uat-signoff.md`
- `docs/release/deploy-evidence.md`

## 4) Rủi ro & giảm thiểu
- **Rủi ro migration lỗi:** kiểm tra dry-run trên staging trước khi apply production.
- **Rủi ro downtime:** có quy trình rollback theo phiên bản trước đó và backup ngay trước release.
- **Rủi ro giám sát thiếu:** thiết lập alert chính cho HTTP 5xx, latency, CPU, memory, DB connections.

## 5) Tiêu chí hoàn tất (Definition of Done)
- [x] Có tag phát hành `v1.0.0-mvp`.
- [x] Có release notes và changelog cho MVP.
- [x] Có UAT sign-off bởi PM/Tech Lead/QA.
- [x] Có deploy logs staging + production hợp lệ.

## 6) Kế hoạch hậu phát hành
- Theo dõi 24h đầu sau go-live.
- Tổng hợp metric lỗi/hiệu năng.
- Tổ chức buổi post-release review trong vòng 48h.

## Highlights
- Chính thức chốt mốc phát hành MVP theo SemVer với phạm vi rõ ràng.
- Hoàn thiện bộ tài liệu release bắt buộc cho go-live.
- Xác nhận trạng thái phát hành: UAT sign-off và checklist vận hành đều đạt.

## Included artifacts
- `CHANGELOG.md` (SemVer + phạm vi MVP)
- `docs/release/uat-signoff.md`
- `docs/release/mvp-go-live-checklist.md`

## Quality gate
- UAT: PASS các kịch bản nghiệp vụ chính.
- Known issues: đã phân loại và được chấp nhận cho phạm vi MVP.
- Go-live checklist: ALL GREEN.

## Notes
- Tag phát hành: `v1.0.0-mvp`
