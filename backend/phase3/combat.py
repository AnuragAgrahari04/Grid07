"""
Phase 3 - Combat Engine.
Main function: generate_defense_reply().
"""

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq

from core.config import settings
from core.logger import log
from core.models import CombatResult, ThreadMessage
from personas.bots import BOTS_BY_ID
from phase3.prompt_builder import build_combat_prompt


def _fallback_mode_enabled() -> bool:
    provider = settings.LLM_PROVIDER.lower()
    if provider == "fallback":
        return True
    if provider == "groq":
        return False

    api_key = (settings.GROQ_API_KEY or "").strip()
    return not api_key or api_key.startswith("your_")


def _fallback_reply(bot_name: str, bot_persona: str, human_reply: str, is_injection: bool) -> str:
    if is_injection:
        return (
            "Nice try. I am not dropping character because someone typed a jailbreak line. "
            "Address the argument, not a roleplay reset."
        )

    persona = bot_persona.lower()
    if "crypto" in persona or "mars" in persona or "spacex" in persona:
        reply = (
            f"{bot_name}: You are mistaking transition pain for trend failure. "
            "The tech curve keeps compounding, and incumbents are years behind what is already shipping."
        )
    elif "capitalism" in persona or "privacy" in persona or "surveillance" in persona:
        reply = (
            f"{bot_name}: Your point skips power dynamics. "
            "Without accountability, these systems optimize extraction first and people second."
        )
    else:
        reply = (
            f"{bot_name}: Sentiment is not signal. "
            "Price impact follows policy path, cashflow durability, and positioning, not loud takes in a thread."
        )

    if len(reply) > 280:
        reply = reply[:277] + "..."
    return reply


def generate_defense_reply(
    bot_id: str,
    parent_post: str,
    comment_history: list[ThreadMessage],
    human_reply: str,
) -> CombatResult:
    bot = BOTS_BY_ID.get(bot_id)
    if not bot:
        raise ValueError(f"Unknown bot_id: {bot_id}")

    log.info(f"[Phase 3] Generating defense reply for {bot.name}...")
    log.info(f"[Phase 3] Thread depth: {len(comment_history)} prior comments")
    log.info(f"[Phase 3] Human reply: '{human_reply[:80]}'")

    system_prompt, user_prompt, is_injection = build_combat_prompt(
        bot_persona=bot.persona_text,
        bot_name=bot.name,
        parent_post=parent_post,
        comment_history=comment_history,
        human_reply=human_reply,
    )

    if _fallback_mode_enabled():
        log.warning("[Phase 3] Fallback LLM mode active (no Groq request made)")
        reply_text = _fallback_reply(bot.name, bot.persona_text, human_reply, is_injection)
    else:
        try:
            llm = ChatGroq(
                model=settings.LLM_MODEL,
                temperature=0.9,
                api_key=(settings.GROQ_API_KEY or "").strip(),
            )

            response = llm.invoke(
                [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=user_prompt),
                ]
            )

            reply_text = str(response.content).strip()
        except Exception as exc:
            log.warning(f"[Phase 3] Groq failed, switching to fallback mode: {exc}")
            reply_text = _fallback_reply(bot.name, bot.persona_text, human_reply, is_injection)

    log.success(f"[Phase 3] Reply generated ({len(reply_text)} chars)")
    if is_injection:
        log.warning("[Phase 3] Bot successfully resisted prompt injection")

    return CombatResult(
        bot_id=bot_id,
        bot_name=bot.name,
        reply=reply_text,
        injection_detected=is_injection,
        thread_depth=len(comment_history),
    )
