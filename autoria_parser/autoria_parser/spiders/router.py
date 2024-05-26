from fastapi import APIRouter, Depends, Security, HTTPException
from auth.base_config import fastapi_users
from auth.models import User
from .database import session_factory
import datetime
# from auth.base_config import fastapi_users
from sqlalchemy import select
from .models import CarItem
from .schemas import GetCarItem
from sqlalchemy import Integer, and_, cast, func, insert, inspect, or_, select, text, String, between
from dateutil.relativedelta import relativedelta
from .queries import CarORM
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis
import subprocess
import os

router = APIRouter(
    prefix="/cars",
    tags=["Cars"]
)


current_active_user = fastapi_users.current_user(active=True)


@router.post("/run-spider/", status_code=201, description="Parses first 10 pages with cars info from auto.ria and"
                                                          " saves a data to database")
def run_spider(user: User = Security(current_active_user)):
    os.chdir('C:/Users/Артем/PycharmProjects/testTask/autoria_parser')
    result = subprocess.run(['scrapy', 'crawl', 'cars'], capture_output=True, text=True)
    return {"stdout": result.stdout, "stderr": result.stderr}


@router.get("/", status_code=200, description="Returns all car items which were parsed from auto.ria and saved in DB")
@cache(expire=86400)
def get_all_cars_data(user: User = Security(current_active_user)):
    with session_factory() as session:
        query = select(CarItem)
        car_items = session.execute(query)
        result_list = car_items.scalars().all()
        return [GetCarItem(id=result_list[item_id].id,
                           url=result_list[item_id].url,
                           title=result_list[item_id].title,
                           price_in_eur=result_list[item_id].price_in_eur,
                           brand=result_list[item_id].brand,
                           model=result_list[item_id].model,
                           year=result_list[item_id].year,
                           region=result_list[item_id].region,
                           mileage=result_list[item_id].mileage,
                           color=result_list[item_id].color,
                           cabin_color=result_list[item_id].cabin_color,
                           cabin_material=result_list[item_id].cabin_material,
                           ad_creation_date=result_list[item_id].ad_creation_date,
                           seller_contacts=result_list[item_id].seller_contacts,
                           created_at=result_list[item_id].created_at) for item_id in range(0, len(result_list))]


@router.get("/min-price/{brand}/{model}", status_code=200, description="Returns the lowest price by brand and model")
@cache(expire=86400)
def min_price_by_brand_and_model(brand: str, model: str, user: User = Security(current_active_user)):
    return CarORM.min_price_by_brand_and_model(brand=brand, model=model)


@router.get("/max-price/{brand}/{model}", status_code=200, description="Returns the highest price by brand and model")
@cache(expire=86400)
def max_price_by_brand_and_model(brand: str, model: str, user: User = Security(current_active_user)):
    return CarORM.max_price_by_brand_and_model(brand=brand, model=model)


@router.get("/by-day/{brand}/{model}", status_code=200, description="Returns number of cars which were added "
                                                                    "to auto.ria during last 24h by brand and model")
@cache(expire=86400)
def cars_daily_count_by_brand_and_model(brand: str, model: str, user: User = Security(current_active_user)):
    return CarORM.get_daily_cars_count_brand_and_model(brand=brand, model=model)


@router.get("/weekly/{brand}/{model}", status_code=200, description="Returns number of cars which were added to"
                                                                    " auto.ria during last 7 days by brand and model")
@cache(expire=86400)
def cars_weekly_count_by_brand_and_model(brand: str, model: str, user: User = Security(current_active_user)):
    return CarORM.get_weekly_cars_count_brand_and_model(brand=brand, model=model)


@router.get("/monthly/{brand}/{model}", status_code=200, description="Returns number of cars which were added to "
                                                                     "auto.ria during last month by brand and model")
@cache(expire=86400)
def cars_monthly_count_by_brand_and_model(brand: str, model: str, user: User = Security(current_active_user)):
    return CarORM.get_monthly_cars_count_brand_and_model(brand=brand, model=model)


@router.get("car/statistics/{brand}/{model}", status_code=200, description="Returns full statistics: minimal price, "
                                                                           "maximal price, count by day / week / month")
@cache(expire=86400)
def get_full_statistics_by_brand_and_model(brand: str, model: str, user: User = Security(current_active_user)):
    return CarORM.get_full_statistics_by_brand_and_model(brand=brand, model=model)
