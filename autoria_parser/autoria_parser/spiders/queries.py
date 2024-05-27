from .database import session_factory
import datetime
from .models import CarItem
from .schemas import GetCarItem
from sqlalchemy import Integer, and_, cast, func, insert, inspect, or_, select, text, String, between
from dateutil.relativedelta import relativedelta
from fastapi_cache.decorator import cache
from sqlalchemy.orm import aliased, contains_eager, joinedload, selectinload


class CarORM:

    @staticmethod
    def get_car_details_by_url(url):
        with session_factory() as session:
            query = (
                select(CarItem)
                .select_from(CarItem)
                .filter(CarItem.url.contains(url))
            )

            query_result = session.execute(query)
            result_list = query_result.scalars().all()
            if result_list:
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
            else:
                return {"Sorry! There are no items with submitted url in DB"}

    @staticmethod
    def get_all_cars_by_time_period(date_from, date_to):
        with session_factory() as session:
            query = (
                select(CarItem)
                .select_from(CarItem)
                .filter(CarItem.ad_creation_date.between(date_from, date_to))
            )
            car_items = session.execute(query)
            result_list = car_items.scalars().all()
            if result_list:
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
            else:
                return {"Sorry, there are no cars in given period in DB!"}


    @staticmethod
    def min_price_by_brand_and_model(brand, model):
        with session_factory() as session:
            query = (
                select(
                    func.min(CarItem.price_in_eur).cast(Integer).label("min_price"),
                )
                .select_from(CarItem)
                .filter(and_(CarItem.model == model, CarItem.brand == brand))
            )
            query_result = session.execute(query)
            result = query_result.scalars().one()
            if result:
                return {
                    "brand": brand,
                    "model": model,
                    "min_price": int(result)
                }
            else:
                return {"Sorry, cars with this brand and model are not found in DB"}

    @staticmethod
    def max_price_by_brand_and_model(brand, model):
        with session_factory() as session:
            query = (
                select(
                    func.max(CarItem.price_in_eur).cast(Integer).label("max_price"),
                )
                .select_from(CarItem)
                .filter(and_(CarItem.model == model, CarItem.brand == brand))
            )
            query_result = session.execute(query)
            result = query_result.scalars().one()
            if result:
                return {
                    "brand": brand,
                    "model": model,
                    "min_price": int(result)
                }
            else:
                return {"Sorry, cars with this brand and model are not found in DB"}

    @staticmethod
    def get_daily_cars_count_brand_and_model(brand, model):
        with session_factory() as session:
            query = (
                select(
                    func.count(CarItem.id).cast(Integer).label("cars_count"),
                )
                .select_from(CarItem)
                .filter(and_(CarItem.model == model,
                             CarItem.brand == brand,
                             CarItem.ad_creation_date.between(datetime.date.today() - datetime.timedelta(days=1),
                                                              datetime.date.today())
                             ))
            )

            query_result = session.execute(query)
            result = query_result.scalars().one()
            if result:
                return {
                    "brand": brand,
                    "model": model,
                    "count_daily": int(result),
                    "date_range_from": datetime.date.today() - datetime.timedelta(days=1),
                    "date_range_to": datetime.date.today()
                }
            else:
                return {"Sorry, cars with this brand and model are not found in DB"}

    @staticmethod
    def get_weekly_cars_count_brand_and_model(brand, model):
        with session_factory() as session:
            query = (
                select(
                    func.count(CarItem.id).cast(Integer).label("cars_count"),
                )
                .select_from(CarItem)
                .filter(and_(CarItem.model == model,
                             CarItem.brand == brand,
                             CarItem.ad_creation_date.between(datetime.date.today() - datetime.timedelta(weeks=1),
                                                              datetime.date.today())
                             ))
            )

            query_result = session.execute(query)
            result = query_result.scalars().one()
            if result:
                return {
                    "brand": brand,
                    "model": model,
                    "count_weekly": int(result),
                    "date_range_from": datetime.date.today() - datetime.timedelta(weeks=1),
                    "date_range_to": datetime.date.today()
                }
            else:
                return {"Sorry, cars with this brand and model are not found in DB"}

    @staticmethod
    def get_monthly_cars_count_brand_and_model(brand, model):
        with session_factory() as session:
            query = (
                select(
                    func.count(CarItem.id).cast(Integer).label("cars_count"),
                )
                .select_from(CarItem)
                .filter(and_(CarItem.model == model,
                             CarItem.brand == brand,
                             CarItem.ad_creation_date.between(datetime.date.today() - relativedelta(months=1),
                                                              datetime.date.today())
                             ))
            )

            query_result = session.execute(query)
            result = query_result.scalars().one()
            if result:
                return {
                    "brand": brand,
                    "model": model,
                    "count_monthly": int(result),
                    "date_range_from": datetime.date.today() - relativedelta(months=1),
                    "date_range_to": datetime.date.today()
                }
            else:
                return {"Sorry, cars with this brand and model are not found in DB"}

    @staticmethod
    def get_full_statistics_by_brand_and_model(brand, model):
        with session_factory() as session:
            min_price_query = (
                select(
                    func.min(CarItem.price_in_eur).cast(Integer).label("min_price"),
                )
                .select_from(CarItem)
                .filter(and_(CarItem.model == model, CarItem.brand == brand))
            )
            min_price_query_result = session.execute(min_price_query)
            min_price_result = min_price_query_result.scalars().one()


            max_price_query = (
                select(
                    func.max(CarItem.price_in_eur).cast(Integer).label("max_price"),
                )
                .select_from(CarItem)
                .filter(and_(CarItem.model == model, CarItem.brand == brand))
            )
            max_price_query_result = session.execute(max_price_query)
            max_price_result = max_price_query_result.scalars().one()

            daily_count_query = (
                select(
                    func.count(CarItem.id).cast(Integer).label("cars_count"),
                )
                .select_from(CarItem)
                .filter(and_(CarItem.model == model,
                             CarItem.brand == brand,
                             CarItem.ad_creation_date.between(datetime.date.today() - datetime.timedelta(days=1),
                                                              datetime.date.today())
                             ))
            )

            daily_count_query_result = session.execute(daily_count_query)
            daily_count_result = daily_count_query_result.scalars().one()

            weekly_count_query = (
                select(
                    func.count(CarItem.id).cast(Integer).label("cars_count"),
                )
                .select_from(CarItem)
                .filter(and_(CarItem.model == model,
                             CarItem.brand == brand,
                             CarItem.ad_creation_date.between(datetime.date.today() - datetime.timedelta(weeks=1),
                                                              datetime.date.today())
                             ))
            )

            weekly_count_query_result = session.execute(weekly_count_query)
            weekly_count_result = weekly_count_query_result.scalars().one()

            monthly_count_query = (
                select(
                    func.count(CarItem.id).cast(Integer).label("cars_count"),
                )
                .select_from(CarItem)
                .filter(and_(CarItem.model == model,
                             CarItem.brand == brand,
                             CarItem.ad_creation_date.between(datetime.date.today() - relativedelta(months=1),
                                                              datetime.date.today())
                             ))
            )

            monthly_count_query_result = session.execute(monthly_count_query)
            monthly_count_result = monthly_count_query_result.scalars().one()

            if min_price_result:

                return {
                    "brand": brand,
                    "model": model,
                    "min_price": int(min_price_result),
                    "max_price": int(max_price_result),
                    "daily_count": {
                        "count": int(daily_count_result),
                        "date_range_from": datetime.date.today() - datetime.timedelta(days=1),
                        "date_range_to": datetime.date.today()
                    },
                    "weekly_count": {
                        "count": int(weekly_count_result),
                        "date_range_from": datetime.date.today() - datetime.timedelta(weeks=1),
                        "date_range_to": datetime.date.today()
                    },
                    "monthly_count": {
                        "count": int(monthly_count_result),
                        "date_range_from": datetime.date.today() - relativedelta(months=1),
                        "date_range_to": datetime.date.today()
                    }

                }
            else:
                return {"Sorry, cars with this brand and model are not found in DB"}