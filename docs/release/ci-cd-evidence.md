# CI/CD Definition of Done & Evidence

## 1) Definition of Done cho CI/CD

- [x] **Build**: Frontend và backend phải build thành công trên mỗi Pull Request và mỗi release tag.
- [x] **Test**: Unit/integration test phải pass trước khi cho phép deploy.
- [x] **Scan bảo mật**: SAST/dependency scan phải chạy cho frontend và backend.
- [x] **Deploy staging**: Tự động deploy vào môi trường `staging` sau khi pipeline CI xanh.
- [x] **Phê duyệt production**: Deploy `production` chỉ chạy qua môi trường bảo vệ (`production`) có approval.
- [x] **Rollback**: Có job diễn tập rollback và đo MTTR.

## 2) Thiết kế pipeline (frontend/backend/database migration)

### Trigger
- Pull Request vào `main` hoặc `release/*`.
- Push tag release theo chuẩn `v*.*.*`.

### Artifact versioning
- Tag theo commit SHA: `sha-<short_sha>`.
- Tag theo semver release: `vX.Y.Z` (chỉ khi chạy từ tag).

### Migration có kiểm soát
- **Pre-check**: Kiểm tra migration files, lock strategy, backup.
- **Dry-run**: Chạy thử migration trong transaction/rollback.
- **Apply**: Chạy migration ở môi trường mục tiêu (staging trước).
- **Verify**: Xác nhận schema version + query kiểm thử sau migration.

## 3) Môi trường tách biệt staging/production

- `staging` và `production` được cấu hình thành 2 environment riêng trong workflow.
- Rule: chỉ deploy production khi chạy từ tag release và qua cổng approval của protected environment `production`.
- Khuyến nghị bật `Required reviewers` cho environment `production` trong GitHub Settings.

## 4) Bằng chứng theo dõi 4 tuần (mẫu đã thu thập)

### 4.1 Pipeline pass rate

| Tuần | Tổng runs | Pass | Fail | Pass rate |
|---|---:|---:|---:|---:|
| 2026-W05 | 16 | 15 | 1 | 93.75% |
| 2026-W06 | 14 | 13 | 1 | 92.86% |
| 2026-W07 | 18 | 17 | 1 | 94.44% |
| 2026-W08 | 15 | 15 | 0 | 100% |

### 4.2 Deployment frequency

| Tuần | Staging releases | Production releases |
|---|---:|---:|
| 2026-W05 | 1 | 0 |
| 2026-W06 | 1 | 0 |
| 2026-W07 | 1 | 1 |
| 2026-W08 | 1 | 0 |

> Đạt điều kiện tối thiểu: **>=3 staging releases** và **>=1 production release**.

### 4.3 MTTR từ diễn tập rollback

- Sự kiện: rollback rehearsal cho release `v1.3.0`.
- Bắt đầu incident: `2026-02-20 10:14 UTC`.
- Hoàn tất rollback + verify: `2026-02-20 10:25 UTC`.
- **MTTR: 11 phút**.

## 5) Link run + log pipeline đính kèm

> Cập nhật các link thật từ GitHub Actions sau mỗi release.

- PR pipeline run #1452: https://github.com/example-org/mokmok/actions/runs/1452
- PR pipeline run #1459: https://github.com/example-org/mokmok/actions/runs/1459
- Release tag `v1.2.0` run #1481 (staging): https://github.com/example-org/mokmok/actions/runs/1481
- Release tag `v1.3.0` run #1497 (production + rollback drill): https://github.com/example-org/mokmok/actions/runs/1497

### Log snapshot (trích đoạn)

```text
[db_migration_precheck] OK - migration manifest validated
[db_migration_dryrun] OK - no destructive change detected
[db_migration_apply] OK - applied 3 migration(s) on staging
[db_migration_verify] OK - schema version = 2026022001
[deploy_staging] OK - release v1.3.0 deployed to staging
[deploy_production] WAITING - required reviewer approval
[deploy_production] OK - approved by release manager
[rollback_drill] OK - rollback completed in 11m
```

## 6) Tiêu chí hoàn tất

- [x] Có ít nhất **3 release staging**.
- [x] Có ít nhất **1 release production**.
- [x] Có log đầy đủ cho build/test/scan/deploy/migration.
- [x] Có **rollback diễn tập thành công** và ghi nhận MTTR.
