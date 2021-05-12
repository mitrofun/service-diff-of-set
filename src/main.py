from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.config import settings
from src.db import database, metadata, engine
from src.api import app_router

app = FastAPI()

metadata.create_all(engine)
app.state.database = database

app.mount('/media', StaticFiles(directory=settings.media_dir), name='media')


@app.on_event("startup")
async def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()

app.include_router(app_router)
