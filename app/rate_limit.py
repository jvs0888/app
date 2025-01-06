import contextlib
from pathlib import Path
import redis.asyncio as redis
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter

try:
    from utils.decorators import utils
    from settings.config import config
except ImportError as ie:
    exit(f'{ie} :: {Path(__file__).resolve()}')


@contextlib.asynccontextmanager
async def rate_limit(_: FastAPI) -> None:
    redis_client: redis.client.Redis = redis.from_url(url=config.DB_CONNECT['redis'], encoding='utf8')
    await FastAPILimiter.init(redis=redis_client)
    yield
    await FastAPILimiter.close()
