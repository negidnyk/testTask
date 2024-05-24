from fastapi import FastAPI

from auth.base_config import auth_backend, fastapi_users
from cars import router as cars_router

app = FastAPI(
    title="Scraper"
)


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

current_user = fastapi_users.current_user()

app.include_router(cars_router)

