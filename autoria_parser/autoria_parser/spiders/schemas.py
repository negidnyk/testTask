from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


# class ModelName(str, Enum):
#     audi = "audi"
#     bmw = "bmw"
#     peugeot = "peugeot"

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
    ad_creation_date: str = None
    seller_contacts: str = None
    created_at: datetime

    class Config:
        orm_mode = True


class GetStatistics(GetCarItem):
    brand: str = None
    model: str = None







# class UpdatePost(BaseModel):
#     title: str = Field(max_length=1500, example="My awesome post!")
#     description: str = Field(max_length=1500, example="Some text to be attached to the post")
#
#
# class PostCreator(BaseModel):
#     id: int
#     name: str
#
#     class Config:
#         orm_mode = True
#
#
# class BasePost(BaseModel):
#     id: int
#     title: str
#     description: str
#     created_at: datetime
#     is_liked: bool
#     likes_count: int
#     comments_count: int
#
#     class Config:
#         orm_mode = True
#
#
# class PostOut(BasePost):
#     creator: UserGetsUser
#     media: MediaOut
#     # media: MediaOut
#
#     class Config:
#         orm_mode = True
#

