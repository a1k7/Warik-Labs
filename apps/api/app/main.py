from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.health import router as health_router
from app.config import settings


@asynccontextmanager
async def lifespan(_: FastAPI):
    yield


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="India-first personal execution assistant — Phase 1 foundation.",
    docs_url="/docs" if settings.app_env.lower() != "production" else None,
    redoc_url=None,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
)

app.include_router(health_router, prefix="/api/v1")
