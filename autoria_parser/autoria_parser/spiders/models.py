from datetime import datetime
from sqlalchemy import Column, Integer, String, TIMESTAMP, Date
from .database import Base


class CarItem(Base):
    __tablename__ = "car_item"

    id = Column(Integer, primary_key=True, index=True, nullable=False, unique=True)
    url = Column(String(150), nullable=False)
    title = Column(String(100), nullable=True)
    price_in_eur = Column(Integer, nullable=True)
    brand = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)
    year = Column(String(10), nullable=True)
    region = Column(String(150), nullable=True)
    mileage = Column(Integer, nullable=True)
    color = Column(String(50), nullable=True)
    cabin_color = Column(String(50), nullable=True)
    cabin_material = Column(String(50), nullable=True)
    ad_creation_date = Column(Date, nullable=False)
    seller_contacts = Column(String(50), nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
