# Migration Execution Log

> Ghi nhận lịch sử migrate thực tế trên **staging** và **prod**.

## Bảng lịch sử

| Date (UTC) | Environment | Release/Change ID | From Version | To Version | Direction | Result | Duration | Operator | Notes |
|---|---|---|---:|---:|---|---|---|---|---|
| 2026-03-01 02:10 | staging | CHG-2026-031 | 202602250900 | 202603010200 | up | success | 2m40s | oncall.a | Thêm index `idx_orders_created_at`; smoke test pass |
| 2026-03-01 02:20 | staging | CHG-2026-031-RB | 202603010200 | 202602250900 | down | success | 1m35s | oncall.a | Rollback rehearsal để kiểm tra script down |
| 2026-03-02 01:05 | prod | CHG-2026-032 | 202602250900 | 202603010200 | up | success | 3m05s | oncall.b | Theo dõi lock time < 2s, không phát sinh error rate |

## Mẫu ghi log cho lần chạy mới

| Date (UTC) | Environment | Release/Change ID | From Version | To Version | Direction | Result | Duration | Operator | Notes |
|---|---|---|---:|---:|---|---|---|---|---|
| YYYY-MM-DD HH:mm | staging/prod | CHG-XXXX | old | new | up/down | success/failed | XmYs | name | ... |
