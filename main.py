import logging

from App.Router import admin as router_admin

from fastapi import FastAPI
from App.DB import database


APIVER = '1.0.0'


def setup_fastapi():
    app = FastAPI()

    app.include_router(
        router_admin.router,
        tags=["admin"],
        prefix="/admin"
    )

    return app


app = setup_fastapi()


@app.on_event("startup")
async def startup():
    await database.Database.database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.Database.database.disconnect()

