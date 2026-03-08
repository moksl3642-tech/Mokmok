from __future__ import annotations

from redis import Redis
from rq import Queue, get_current_job

from .config import settings
from .db import SessionFactory
from .repository import BackgroundJobRepository
from .tasks import TASK_REGISTRY

redis_conn = Redis.from_url(settings.redis_url)
dead_letter_queue = Queue(settings.dead_letter_queue_name, connection=redis_conn)


class TemporaryWorkerError(Exception):
    """Use for transient failures that should be retried."""


def execute_task(task_name: str, payload: dict) -> dict:
    job = get_current_job()
    if not job:
        raise RuntimeError("execute_task must run inside an RQ worker")

    return _execute_task_sync(job.id, task_name, payload, job.retries_left)


def _execute_task_sync(job_id: str, task_name: str, payload: dict, retries_left: int | None) -> dict:
    import asyncio

    return asyncio.run(_execute_task(job_id, task_name, payload, retries_left))


async def _execute_task(job_id: str, task_name: str, payload: dict, retries_left: int | None) -> dict:
    async with SessionFactory() as session:
        repo = BackgroundJobRepository(session)
        await repo.mark_running(job_id)

        try:
            task = TASK_REGISTRY[task_name]
            result = task(payload)
            output = {"summary": result.summary, "data": result.data}
            await repo.mark_success(job_id, output)
            return {"status": "success", "result": output}
        except TemporaryWorkerError as exc:
            if retries_left and retries_left > 0:
                raise
            dead_letter_queue.enqueue(record_dead_letter, job_id, task_name, payload, str(exc))
            await repo.mark_failure(job_id, str(exc), retry_count=settings.max_retries)
            raise
        except Exception as exc:
            await repo.mark_failure(job_id, str(exc), retry_count=settings.max_retries)
            dead_letter_queue.enqueue(record_dead_letter, job_id, task_name, payload, str(exc))
            raise


def record_dead_letter(job_id: str, task_name: str, payload: dict, error_message: str) -> dict:
    return {
        "original_job_id": job_id,
        "task_name": task_name,
        "payload": payload,
        "error_message": error_message,
        "queue": settings.dead_letter_queue_name,
    }
