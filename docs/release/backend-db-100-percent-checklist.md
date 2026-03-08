# Backend + DB 100% Release Checklist

Mục tiêu tài liệu này là xác nhận mức hoàn tất phát hành Backend + Database đạt **100%**, với đầy đủ bằng chứng và phê duyệt liên chức năng.

## 1) Functional completeness

| Hạng mục | Tiêu chí pass | Bằng chứng bắt buộc | Trạng thái |
|---|---|---|---|
| API nghiệp vụ cốt lõi | 100% user story/acceptance criteria được implement và verify | Link pipeline build/deploy; report test chức năng; sign-off Tech Lead + QA | ☐ Pass / ☐ Fail |
| Tích hợp liên dịch vụ | Không còn blocker ở các luồng tích hợp (payment, notification, auth, v.v.) | Link pipeline integration; report integration test; dashboard snapshot lỗi = 0 blocker | ☐ Pass / ☐ Fail |
| Regression | Không có lỗi mức Critical/High chưa xử lý | Link pipeline regression; report regression test; sign-off PM | ☐ Pass / ☐ Fail |

## 2) Data integrity

| Hạng mục | Tiêu chí pass | Bằng chứng bắt buộc | Trạng thái |
|---|---|---|---|
| Migration schema | Toàn bộ migration chạy thành công ở staging/prod rehearsal | Migration log; link pipeline DB migration; sign-off DevOps | ☐ Pass / ☐ Fail |
| Ràng buộc dữ liệu | PK/FK/unique/check/index đúng thiết kế và không phát sinh sai lệch | Report kiểm tra tính nhất quán; dashboard snapshot DB health; sign-off Tech Lead | ☐ Pass / ☐ Fail |
| Backup/restore dữ liệu | Restore thử nghiệm thành công với dữ liệu đại diện | Log backup/restore; report kiểm thử phục hồi dữ liệu; sign-off QA + DevOps | ☐ Pass / ☐ Fail |

## 3) Security compliance

| Hạng mục | Tiêu chí pass | Bằng chứng bắt buộc | Trạng thái |
|---|---|---|---|
| Quét lỗ hổng ứng dụng/phụ thuộc | Không còn lỗ hổng Critical/High chưa có mitigation được duyệt | Link pipeline security scan (SAST/SCA); report scan; sign-off Security | ☐ Pass / ☐ Fail |
| Bảo mật dữ liệu | Secrets được quản lý đúng chuẩn; dữ liệu nhạy cảm được mã hóa theo chính sách | Report kiểm tra cấu hình bảo mật; dashboard snapshot secret/compliance; sign-off Security + DevOps | ☐ Pass / ☐ Fail |
| Kiểm soát truy cập | Phân quyền và audit log đáp ứng yêu cầu | Report test authorization/audit; link pipeline test; sign-off Security + QA | ☐ Pass / ☐ Fail |

## 4) Performance/SLO compliance

| Hạng mục | Tiêu chí pass | Bằng chứng bắt buộc | Trạng thái |
|---|---|---|---|
| Hiệu năng API | P95/P99 latency và throughput đạt ngưỡng SLO | Report performance test; dashboard snapshot APM; sign-off Tech Lead | ☐ Pass / ☐ Fail |
| Năng lực DB | Query quan trọng đạt baseline; không có truy vấn top slow chưa tối ưu | Report benchmark/query profile; dashboard snapshot DB metrics; sign-off DBA/Tech Lead | ☐ Pass / ☐ Fail |
| Độ ổn định tải | Soak/stress test không gây lỗi vượt error budget | Link pipeline load test; report load/soak; sign-off PM + QA | ☐ Pass / ☐ Fail |

## 5) Operability/DR readiness

| Hạng mục | Tiêu chí pass | Bằng chứng bắt buộc | Trạng thái |
|---|---|---|---|
| Quan sát hệ thống | Dashboard, alert, runbook đầy đủ và đã kiểm thử cảnh báo | Dashboard snapshot observability; report diễn tập cảnh báo; sign-off DevOps | ☐ Pass / ☐ Fail |
| Triển khai & rollback | Quy trình deploy/rollback đã rehearsal thành công | Link pipeline deploy; log rollback rehearsal; sign-off DevOps + Tech Lead | ☐ Pass / ☐ Fail |
| DR readiness | Kịch bản DR đạt RTO/RPO mục tiêu | Report diễn tập DR; migration log liên quan failover; sign-off PM + DevOps + Security | ☐ Pass / ☐ Fail |

---

## Bằng chứng tổng hợp bắt buộc cho mọi nhóm

Mỗi nhóm checklist phải đính kèm đầy đủ 5 loại bằng chứng sau:
1. **Link pipeline** (build/test/deploy/security/load tuỳ hạng mục).
2. **Report test** (functional/integration/regression/security/performance/DR).
3. **Dashboard snapshot** (APM/DB/security/observability).
4. **Migration log** (đối với hạng mục có liên quan DB schema/data).
5. **Sign-off** của vai trò chịu trách nhiệm.

## Tiêu chí hoàn tất (Definition of Done)

Release Backend + DB chỉ được xác nhận hoàn tất khi:
- Tất cả hạng mục trong 5 nhóm đều ở trạng thái **Pass**.
- Có đủ bằng chứng bắt buộc cho từng hạng mục.
- Có chữ ký phê duyệt cuối cùng trong biên bản nghiệm thu.
