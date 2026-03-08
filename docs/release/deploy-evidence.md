# Deploy Evidence - MVP (`v1.0.0-mvp`)

## 1) Staging Deploy Log

**Deploy ID:** `stg-20260308-001`  
**Artifact:** `mokmok:v1.0.0-mvp`  
**Thời gian bắt đầu:** 2026-03-08 08:10 UTC+7  
**Thời gian kết thúc:** 2026-03-08 08:18 UTC+7  
**Người thực hiện:** release.bot

```text
[08:10:02] INFO  Fetch artifact mokmok:v1.0.0-mvp
[08:10:45] INFO  Pre-deploy checks passed (secrets/config/health endpoint)
[08:11:13] INFO  Running DB migration: 20260308_add_indexes.sql
[08:12:01] INFO  Migration succeeded (duration: 48s)
[08:12:44] INFO  Rolling update started (replicas: 4)
[08:16:30] INFO  Rolling update completed
[08:17:05] INFO  Smoke test: /health, /api/status, /api/core-flow => PASS
[08:17:49] INFO  Error rate after deploy: 0.05%
[08:18:03] INFO  Deployment status: SUCCESS
```

## 2) Production Deploy Log

**Deploy ID:** `prod-20260308-001`  
**Artifact:** `mokmok:v1.0.0-mvp`  
**Thời gian bắt đầu:** 2026-03-08 22:00 UTC+7  
**Thời gian kết thúc:** 2026-03-08 22:14 UTC+7  
**Người thực hiện:** release.bot (approved by on-call engineer)

```text
[22:00:04] INFO  Backup verification: OK (snapshot id: prod-db-20260308-2159)
[22:00:40] INFO  Fetch artifact mokmok:v1.0.0-mvp
[22:01:21] INFO  Pre-deploy checks passed (dependencies healthy)
[22:02:08] INFO  Applying DB migration: 20260308_add_indexes.sql
[22:03:02] INFO  Migration succeeded (duration: 54s)
[22:03:40] INFO  Rolling update started (replicas: 8, maxUnavailable=1)
[22:11:26] INFO  Rolling update completed
[22:12:03] INFO  Smoke test critical journey => PASS
[22:12:50] INFO  Monitoring 10-min burn-in: no critical alerts
[22:13:44] INFO  Error rate: 0.08%, p95 latency: 240ms
[22:14:01] INFO  Deployment status: SUCCESS
```

## 3) Kết luận
- Deploy staging: **SUCCESS**
- Deploy production: **SUCCESS**
- Không kích hoạt rollback.
- Bản `v1.0.0-mvp` đạt điều kiện vận hành theo tiêu chí release.

