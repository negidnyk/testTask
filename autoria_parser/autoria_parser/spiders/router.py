from fastapi import APIRouter
from .database import session_factory
from auth.base_config import fastapi_users
from sqlalchemy import select
from .models import CarItem
from .schemas import GetCarItem
from sqlalchemy import Integer, and_, cast, func, insert, inspect, or_, select, text

router = APIRouter(
    prefix="/cars",
    tags=["Cars"]
)


current_active_user = fastapi_users.current_user(active=True)



@router.get("/", status_code=200)
def get_all_cars_data():
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


@router.get("/min-price/{brand}/{model}", status_code=200)
def min_price_by_brand_and_model(brand: str, model: str):
    with session_factory() as session:
        query = select(CarItem).filter(and_(CarItem.model == model, CarItem.brand == brand))
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

        # query = (select(CarItem,
        #         # 1 вариант использования cast
        #         # cast(func.avg(ResumesOrm.compensation), Integer).label("avg_compensation"),
        #         # 2 вариант использования cast (предпочтительный способ)
        #         func.avg(ResumesOrm.compensation).cast(Integer).label("avg_compensation"),
        #     )
        #     .select_from(ResumesOrm)
        #     .filter(and_(
        #         ResumesOrm.title.contains(like_language),
        #         ResumesOrm.compensation > 40000,
        #     ))
        #     .group_by(ResumesOrm.workload)
        #     .having(func.avg(ResumesOrm.compensation) > 70000)
        # )
        # print(query.compile(compile_kwargs={"literal_binds": True}))
        # res = session.execute(query)
        # result = res.all()
        # print(result[0].avg_compensation)
        # return {"Brand": brand, "Model": model}


@router.get("/max-price/{brand}/{model}", status_code=200)
def max_price_by_brand_and_model(brand: str, model: str):
    with session_factory() as session:
        query = select(CarItem).filter(and_(CarItem.model == model, CarItem.brand == brand))
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


@router.get("/by-day/{brand}/{model}", status_code=200)
def cars_daily_count_by_brand_and_model(brand: str, model: str):
    with session_factory() as session:
        query = select(CarItem).filter(and_(CarItem.model == model, CarItem.brand == brand))
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


@router.get("/weekly/{brand}/{model}", status_code=200)
def cars_weekly_count_by_brand_and_model(brand: str, model: str):
    with session_factory() as session:
        query = select(CarItem).filter(and_(CarItem.model == model, CarItem.brand == brand))
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


@router.get("/monthly/{brand}/{model}", status_code=200)
def cars_monthly_count_by_brand_and_model(brand: str, model: str):
    with session_factory() as session:
        query = select(CarItem).filter(and_(CarItem.model == model, CarItem.brand == brand))
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
