from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routers.exception_container import exception_container
from backend.services import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    # shutdown
    await db_helper.dispose()


def create_app() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan,
    )
    origins = [
        'http://localhost',
        'http://localhost:8080',
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
    app = exception_container(app)

    return app
