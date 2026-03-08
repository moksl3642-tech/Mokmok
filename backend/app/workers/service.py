from __future__ import annotations

from dataclasses import dataclass

from redis import Redis
from rq import Queue
from rq.retry import Retry

from .config import settings
from .db import SessionFactory
from .repository import BackgroundJobRepository
from .worker_runner import execute_task


@dataclass
class EnqueueResult:
    job_id: str
    deduplicated: bool


redis_conn = Redis.from_url(settings.redis_url)
queue = Queue(settings.queue_name, connection=redis_conn)


async def enqueue_task(
    *,
    task_name: str,
    payload: dict,
    idempotency_key: str | None = None,
) -> EnqueueResult:
    async with SessionFactory() as session:
        repo = BackgroundJobRepository(session)
        if idempotency_key:
            existing = await repo.get_by_idempotency_key(task_name, idempotency_key)
            if existing:
                return EnqueueResult(job_id=existing.job_id, deduplicated=True)

        rq_job = queue.enqueue(
            execute_task,
            task_name,
            payload,
            retry=Retry(max=settings.max_retries, interval=list(settings.default_retry_intervals)),
        )

        await repo.create_queued(
            job_id=rq_job.id,
            task_name=task_name,
            payload=payload,
            idempotency_key=idempotency_key,
        )

        return EnqueueResult(job_id=rq_job.id, deduplicated=False)
