import os
from dotenv import load_dotenv
from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
AUTH_SECRET = os.environ.get("AUTH_SECRET")
RESET_PASS_SECRET = os.environ.get("RESET_PASS_SECRET")

metadata = MetaData()

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Use declarative base for models
Base = declarative_base()

session_factory = sessionmaker(engine)
