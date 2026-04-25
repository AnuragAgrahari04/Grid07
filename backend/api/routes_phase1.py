"""Phase 1 API routes."""

from fastapi import APIRouter

from core.models import RouteRequest, RoutingResult
from phase1.router import route_post_to_bots

router = APIRouter()


@router.post("/route", response_model=RoutingResult)
async def route_post(payload: RouteRequest) -> RoutingResult:
    return route_post_to_bots(
        post_content=payload.post_content,
        threshold=payload.threshold if payload.threshold is not None else 0.85,
    )
