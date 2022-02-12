import logging

from App.Router import admin as router_admin
from App.Router import user as router_user
from App.Router import auth as router_auth

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

    app.include_router(
        router_admin.router,
        tags=["user"],
        prefix="/user"
    )

    app.include_router(
        router_auth.router,
        tags=["auth"],
        prefix="/auth"
    )

    return app


app = setup_fastapi()


@app.on_event("startup")
async def startup():
    await database.database.database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.database.database.disconnect()

