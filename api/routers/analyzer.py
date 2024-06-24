from typing import Optional
from fastapi import APIRouter, Body, Depends, status
from api.security import get_current_user
from api.routers.models import AnalyzerOutputModel
from api.shared import load_analyzer


analyzer_router = APIRouter(
    prefix="/analyzer",
    tags=["analyzer"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(get_current_user)],
)

analyzers = load_analyzer()


@analyzer_router.post(
    "/sentiment",
    status_code=status.HTTP_200_OK,
    response_model=Optional[AnalyzerOutputModel],
)
async def analyze_hate(
    text: str = Body(..., embed=True, description="Text to analyze"),
):
    return analyzers["sentiment"].predict(text)


@analyzer_router.post(
    "/emotion",
    status_code=status.HTTP_200_OK,
    response_model=Optional[AnalyzerOutputModel],
)
async def analyze_emotion(
    text: str = Body(..., embed=True, description="Text to analyze"),
):
    return analyzers["emotion"].predict(text)
