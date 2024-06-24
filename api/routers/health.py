from typing import Optional
from fastapi import APIRouter, HTTPException, status

from api.db.client import create_supabase_client
from api.routers.models import HealthCheck

health_router = APIRouter(
    prefix="/health",
    tags=["health "],
    responses={404: {"description": "Not found"}},
)


@health_router.get(
    "/", status_code=status.HTTP_200_OK, response_model=Optional[HealthCheck]
)
async def healthcheck():
    client = create_supabase_client()

    if client is None:
        raise HTTPException(status_code=500, detail="Supabase client not created.")

    return HealthCheck(status="ok", message="Service is healthy.")