from fastapi import FastAPI, APIRouter, Security
from auth.schemas import UserRead, UserCreate
from auth.base_config import auth_backend, fastapi_users

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
import subprocess
import os
from auth.models import User
from autoria_parser.autoria_parser.spiders.queries import CarORM
from fastapi_cache.decorator import cache
from pydantic.schema import date


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


current_active_user = fastapi_users.current_user(active=True)


@app.post("/run-spider/", status_code=201, description="Parses first 10 pages with cars info from auto.ria and\
 saves a data to database")
def run_spider(user: User = Security(current_active_user)):
    os.chdir('C:/Users/Артем/PycharmProjects/testTask/autoria_parser')
    result = subprocess.run(['scrapy', 'crawl', 'cars'], capture_output=True, text=True)
    return {"stdout": result.stdout, "stderr": result.stderr}


@app.get("/by_url", status_code=200, description="Returns all car item details by url")
@cache(expire=86400)
def get_all_cars_data_by_url(url: str, user: User = Security(current_active_user)):
    return CarORM.get_car_details_by_url(url)


@app.get("/", status_code=200, description="Returns all car items which were parsed from auto.ria and saved in DB by"
                                              " submitted period of ads creation date. "
                                              "Example of input data: '2024-02-14'")
@cache(expire=86400)
def get_all_cars_data_by_period(date_from: date, date_to: date, user: User = Security(current_active_user)):
    return CarORM.get_all_cars_by_time_period(date_from, date_to)


@app.get("/min-price/{brand}/{model}", status_code=200, description="Returns the lowest price by brand and model")
@cache(expire=86400)
def min_price_by_brand_and_model(brand: str, model: str, user: User = Security(current_active_user)):
    return CarORM.min_price_by_brand_and_model(brand=brand, model=model)


@app.get("/max-price/{brand}/{model}", status_code=200, description="Returns the highest price by brand and model")
@cache(expire=86400)
def max_price_by_brand_and_model(brand: str, model: str, user: User = Security(current_active_user)):
    return CarORM.max_price_by_brand_and_model(brand=brand, model=model)


@app.get("/by-day/{brand}/{model}", status_code=200, description="Returns number of cars which were added "
                                                                    "to auto.ria during last 24h by brand and model")
@cache(expire=86400)
def cars_daily_count_by_brand_and_model(brand: str, model: str, user: User = Security(current_active_user)):
    return CarORM.get_daily_cars_count_brand_and_model(brand=brand, model=model)


@app.get("/weekly/{brand}/{model}", status_code=200, description="Returns number of cars which were added to"
                                                                    " auto.ria during last 7 days by brand and model")
@cache(expire=86400)
def cars_weekly_count_by_brand_and_model(brand: str, model: str, user: User = Security(current_active_user)):
    return CarORM.get_weekly_cars_count_brand_and_model(brand=brand, model=model)


@app.get("/monthly/{brand}/{model}", status_code=200, description="Returns number of cars which were added to "
                                                                     "auto.ria during last month by brand and model")
@cache(expire=86400)
def cars_monthly_count_by_brand_and_model(brand: str, model: str, user: User = Security(current_active_user)):
    return CarORM.get_monthly_cars_count_brand_and_model(brand=brand, model=model)


@app.get("car/statistics/{brand}/{model}", status_code=200, description="Returns full statistics: minimal "
                                                                                "price, maximal price, count by day / "
                                                                                "week / month")
@cache(expire=86400)
def get_full_statistics_by_brand_and_model(brand: str, model: str, user: User = Security(current_active_user)):
    return CarORM.get_full_statistics_by_brand_and_model(brand=brand, model=model)


