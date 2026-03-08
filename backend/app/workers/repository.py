from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import BackgroundJob, JobStatus


class BackgroundJobRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_job_id(self, job_id: str) -> BackgroundJob | None:
        stmt = select(BackgroundJob).where(BackgroundJob.job_id == job_id)
        return await self.session.scalar(stmt)

    async def get_by_idempotency_key(self, task_name: str, idempotency_key: str) -> BackgroundJob | None:
        stmt = select(BackgroundJob).where(
            BackgroundJob.task_name == task_name,
            BackgroundJob.idempotency_key == idempotency_key,
            BackgroundJob.status.in_([JobStatus.QUEUED, JobStatus.RUNNING, JobStatus.SUCCESS]),
        )
        return await self.session.scalar(stmt)

    async def create_queued(
        self,
        *,
        job_id: str,
        task_name: str,
        payload: dict | None,
        idempotency_key: str | None,
    ) -> BackgroundJob:
        record = BackgroundJob(
            job_id=job_id,
            task_name=task_name,
            payload=payload,
            idempotency_key=idempotency_key,
            status=JobStatus.QUEUED,
        )
        self.session.add(record)
        await self.session.commit()
        await self.session.refresh(record)
        return record

    async def mark_running(self, job_id: str) -> None:
        record = await self.get_by_job_id(job_id)
        if not record:
            return
        record.status = JobStatus.RUNNING
        record.started_at = datetime.now(tz=timezone.utc)
        await self.session.commit()

    async def mark_success(self, job_id: str, result: dict | None) -> None:
        record = await self.get_by_job_id(job_id)
        if not record:
            return
        record.status = JobStatus.SUCCESS
        record.result = result
        record.completed_at = datetime.now(tz=timezone.utc)
        await self.session.commit()

    async def mark_failure(self, job_id: str, error_message: str, retry_count: int) -> None:
        record = await self.get_by_job_id(job_id)
        if not record:
            return
        record.status = JobStatus.FAILURE
        record.error_message = error_message
        record.retry_count = retry_count
        record.completed_at = datetime.now(tz=timezone.utc)
        await self.session.commit()
