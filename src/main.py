# ruff: noqa: E402
import logging
import sys
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import uvicorn

sys.path.append(str(Path(__file__).parent.parent))

logging.basicConfig(level=logging.INFO)

from src.init import redis_connector
from src.api.auth import router as router_auth
from src.api.users import router as router_users
from src.api.authors import router as router_authors
from src.api.books import router as router_books
from src.api.borrows import router as router_borrows


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_connector.connect()

    FastAPICache.init(RedisBackend(redis_connector.redis), prefix="fastapi-cache")
    logging.info("FastAPI Cache инициализирован")
    yield
    await redis_connector.close()


app = FastAPI(lifespan=lifespan)

app.include_router(router_auth)
app.include_router(router_users)
app.include_router(router_authors)
app.include_router(router_books)
app.include_router(router_borrows)

if __name__ == "__main__":
    logging.info("Запуск приложения через uvicorn")
    uvicorn.run("main:app", host="", reload=True)
