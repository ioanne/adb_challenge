from fastapi import FastAPI

from app.api.v1.routers import device

app = FastAPI()

app.include_router(device.router)
