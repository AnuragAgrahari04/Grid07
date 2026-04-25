"""Phase 2 API routes."""

from fastapi import APIRouter, HTTPException

from core.models import GenerateRequest, PostOutput
from phase2.engine import run_content_engine

router = APIRouter()


@router.post("/generate", response_model=PostOutput)
async def generate_post(payload: GenerateRequest) -> PostOutput:
    try:
        output = run_content_engine(payload.bot_id)
        return PostOutput.model_validate(output)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Phase 2 generation failed: {exc}") from exc
