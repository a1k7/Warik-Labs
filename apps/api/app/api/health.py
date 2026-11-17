from fastapi import APIRouter, HTTPException
from redis import Redis
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.config import settings
from app.db import engine

router = APIRouter(tags=["health"])


@router.get("/health/live", summary="Liveness probe")
def liveness() -> dict[str, str]:
    return {"status": "alive", "service": "warik-labs-api"}


@router.get("/health/ready", summary="Readiness probe")
def readiness() -> dict[str, str]:
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except SQLAlchemyError as exc:
        raise HTTPException(status_code=503, detail="database_not_ready") from exc

    redis_client = Redis.from_url(settings.redis_url, socket_connect_timeout=1, socket_timeout=1)
    try:
        redis_client.ping()
    except Exception as exc:
        raise HTTPException(status_code=503, detail="queue_not_ready") from exc
    finally:
        redis_client.close()

    return {"status": "ready", "database": "ok", "queue": "ok"}
