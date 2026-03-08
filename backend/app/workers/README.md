# Background workers

This module moves CPU/I/O-heavy tasks out of synchronous API handlers by using **RQ + Redis** workers.

## What is covered
- Queue configuration under `backend/app/workers/`.
- Heavy tasks:
  - `ml.logistic_regression.train`
  - `stats.roadmap.batch_recompute`
- Idempotency-key deduplication to avoid duplicate execution on retries/client replays.
- Retry policy for transient errors (`TemporaryWorkerError`) and dead-letter routing to `dead_letter` queue.
- Durable status tracking in `system.background_jobs` table (`queued/running/success/failure`).

## Enqueue from API layer

```python
from app.workers import enqueue_task

result = await enqueue_task(
    task_name="ml.logistic_regression.train",
    payload={"records": 120000, "penalty": "l2"},
    idempotency_key="request-uuid-123"
)
```

If the same idempotency key is sent again for the same task and previous job is queued/running/success, the existing job id is returned.

## Running workers

```bash
python -m backend.app.workers.worker
```

## Tracing failures
- `system.background_jobs.error_message` keeps failure reason.
- `retry_count` records terminal retry count.
- Failed terminal jobs are copied to `dead_letter` queue payload for post-mortem handling.

This architecture keeps API request latency stable under load because expensive work is acknowledged quickly then processed asynchronously.
