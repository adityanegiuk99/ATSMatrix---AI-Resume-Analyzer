from redis import Redis
from rq import Queue, Worker
from app.core.config import settings

redis = Redis.from_url(settings.redis_url)
resume_queue = Queue("resume-processing", connection=redis, default_timeout=600)


def run_worker() -> None:
    Worker([resume_queue], connection=redis).work()


if __name__ == "__main__":
    run_worker()
