"""Phase 3 API routes."""

from fastapi import APIRouter, HTTPException

from core.models import CombatRequest, CombatResult
from phase3.combat import generate_defense_reply

router = APIRouter()


@router.post("/defend", response_model=CombatResult)
async def defend(payload: CombatRequest) -> CombatResult:
    try:
        return generate_defense_reply(
            bot_id=payload.bot_id,
            parent_post=payload.parent_post,
            comment_history=payload.comment_history,
            human_reply=payload.human_reply,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Phase 3 defense failed: {exc}") from exc
