import logging

from App.Router import admin as router_admin
from App.Router import user as router_user
from App.Router import auth as router_auth

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from App.DB import database


APIVER = '1.0.0'


def setup_fastapi():
    app = FastAPI()

    origins = [
        "http://localhost:3000",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["POST", "GET", "OPTIONS"],
        allow_headers=["*"],
    )

    app.include_router(
        router_admin.router,
        tags=["admin"],
        prefix="/admin"
    )

    app.include_router(
        router_user.router,
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

