# Environment Promotion Policy

## Environments

- `staging`: auto-deploy từ PR/release tag để UAT.
- `production`: chỉ deploy từ release tag `v*.*.*`.

## Production approval rule

1. Bật **Protected Environment** cho `production` trên GitHub.
2. Cấu hình **Required reviewers** (Release Manager + Tech Lead).
3. Chỉ job `deploy_production` mới dùng environment `production`.
4. Nếu chưa có approval, workflow dừng ở trạng thái `Waiting`.

## Rollback

- Luôn giữ release trước đó để rollback nhanh.
- Sau rollback phải chạy verify healthcheck và smoke test.
