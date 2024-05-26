from fastapi import FastAPI
from auth.schemas import UserRead, UserCreate
from auth.base_config import auth_backend, fastapi_users
from autoria_parser.autoria_parser.spiders.router import router as cars_router

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis


app = FastAPI(
    title="Scraper"
)


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)


current_user = fastapi_users.current_user()


app.include_router(cars_router)

