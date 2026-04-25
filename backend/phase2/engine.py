"""Public interface for Phase 2 content generation."""

from core.models import PostOutput
from personas.bots import BOTS_BY_ID
from phase2.graph import run_graph


def run_content_engine(bot_id: str) -> dict:
    bot = BOTS_BY_ID.get(bot_id)
    if not bot:
        raise ValueError(f"Unknown bot_id: {bot_id}")

    output = run_graph(bot_id=bot_id, bot_persona=bot.persona_text)
    validated = PostOutput.model_validate(output)
    return validated.model_dump()
