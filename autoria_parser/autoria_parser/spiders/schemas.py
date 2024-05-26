from pydantic import BaseModel, Field
from datetime import datetime
from pydantic.schema import date


class GetCarItem(BaseModel):

    id: int
    url: str
    title: str
    price_in_eur: str
    brand: str = None
    model: str = None
    year: str = None
    region: str = None
    mileage: str = None
    color: str = None
    cabin_color: str = None
    cabin_material: str = None
    ad_creation_date: date = None
    seller_contacts: str = None
    created_at: datetime

    class Config:
        orm_mode = True


class GetStatistics(GetCarItem):
    brand: str = None
    model: str = None




