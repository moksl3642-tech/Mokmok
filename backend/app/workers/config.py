from dataclasses import dataclass
import os


@dataclass(frozen=True)
class WorkerSettings:
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    queue_name: str = os.getenv("WORKER_QUEUE_NAME", "default")
    dead_letter_queue_name: str = os.getenv("WORKER_DEAD_LETTER_QUEUE", "dead_letter")
    default_retry_intervals: tuple[int, ...] = (30, 120, 300)
    max_retries: int = int(os.getenv("WORKER_MAX_RETRIES", "3"))


settings = WorkerSettings()
