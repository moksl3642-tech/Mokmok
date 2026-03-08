from redis import Redis
from rq import Connection, Queue, Worker

from .config import settings


def run() -> None:
    conn = Redis.from_url(settings.redis_url)
    with Connection(conn):
        worker = Worker(
            [Queue(settings.queue_name), Queue(settings.dead_letter_queue_name)],
            connection=conn,
        )
        worker.work(with_scheduler=True)


if __name__ == "__main__":
    run()
