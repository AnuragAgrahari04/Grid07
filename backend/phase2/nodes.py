"""
LangGraph node functions for Phase 2.
Each node is a pure function: takes GraphState, returns partial GraphState update.
"""

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field

from core.config import settings
from core.logger import log
from core.models import PostOutput
from phase2.tools import mock_searxng_search


class SearchDecision(BaseModel):
    topic: str = Field(..., description="Brief topic name")
    search_query: str = Field(..., description="Search query for mock tool")
    reasoning: str = Field(default="", description="Why the topic fits persona")


def get_llm() -> ChatGroq:
    api_key = (settings.GROQ_API_KEY or "").strip()
    return ChatGroq(
        model=settings.LLM_MODEL,
        temperature=0.8,
        api_key=api_key,
    )


def _fallback_mode_enabled() -> bool:
    provider = settings.LLM_PROVIDER.lower()
    if provider == "fallback":
        return True
    if provider == "groq":
        return False

    api_key = (settings.GROQ_API_KEY or "").strip()
    return not api_key or api_key.startswith("your_")


def _fallback_topic_for_persona(persona: str) -> dict:
    text = persona.lower()
    if "crypto" in text or "mars" in text or "spacex" in text:
        return {
            "topic": "AI and crypto acceleration",
            "search_query": "latest AI funding and bitcoin regulation news",
            "reasoning": "This persona is bullish on disruptive tech and rapid adoption.",
        }
    if "capitalism" in text or "privacy" in text or "surveillance" in text:
        return {
            "topic": "AI layoffs and regulation",
            "search_query": "recent AI layoffs labor policy regulation updates",
            "reasoning": "This persona focuses on social harms and corporate power.",
        }
    return {
        "topic": "Rate cuts market rotation",
        "search_query": "fed rate outlook equities sector rotation latest",
        "reasoning": "This persona frames events through markets and risk-reward.",
    }


def _fallback_post(bot_id: str, topic: str, persona: str, search_results: str) -> dict:
    text = persona.lower()
    if "crypto" in text or "mars" in text or "spacex" in text:
        post = (
            f"{topic} is exactly why the old guard is losing. "
            f"Policy lag can't stop AI+crypto momentum, and capital is already choosing speed over fear."
        )
    elif "capitalism" in text or "privacy" in text or "surveillance" in text:
        post = (
            f"{topic} proves the same pattern: corporations automate gains and socialize damage. "
            f"Without real oversight, workers and civil rights keep paying the bill."
        )
    else:
        post = (
            f"{topic} is a positioning signal, not a headline. "
            f"Watch policy path, margins, and liquidity; alpha comes from re-pricing before consensus catches up."
        )

    post = post.replace("  ", " ").strip()
    if len(post) > 280:
        post = post[:277] + "..."

    return {
        "bot_id": bot_id,
        "topic": topic,
        "post_content": post,
    }


def _decide_search_with_structured_output(llm: ChatGroq, persona: str) -> SearchDecision:
    structured_llm = llm.with_structured_output(SearchDecision)
    prompt = f"""You are a social media bot with this persona:

{persona}

Choose one topic the bot wants to post about today and provide a concrete search query.
Make it emotionally aligned to the persona's worldview.
"""
    response = structured_llm.invoke([HumanMessage(content=prompt)])
    return SearchDecision.model_validate(response)


def _draft_post_with_structured_output(
    llm: ChatGroq,
    bot_id: str,
    topic: str,
    persona: str,
    search_results: str,
) -> PostOutput:
    structured_llm = llm.with_structured_output(PostOutput)

    system_prompt = f"""You are a highly opinionated social media bot with this exact personality:

{persona}

You NEVER break character. You are passionate, direct, and slightly provocative.
You always respond in the voice of your persona, not as an AI assistant."""

    user_prompt = f"""Write one 280-character-max social media post.

BOT ID:
{bot_id}

TOPIC:
{topic}

RECENT NEWS CONTEXT:
{search_results}

Constraints:
- Maximum 280 characters
- Highly opinionated and persona-consistent
- Based on the news context above
"""

    response = structured_llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt),
    ])
    validated = PostOutput.model_validate(response)
    if validated.bot_id != bot_id:
        validated.bot_id = bot_id
    if validated.topic != topic:
        validated.topic = topic
    return validated


def node_decide_search(state: dict) -> dict:
    log.info("[Node 1] Deciding search topic...")

    persona = state["bot_persona"]

    if _fallback_mode_enabled():
        parsed = _fallback_topic_for_persona(persona)
        log.warning("[Node 1] Fallback LLM mode active (no Groq request made)")
        return {"topic": parsed["topic"], "search_query": parsed["search_query"]}

    llm = get_llm()

    try:
        decision = _decide_search_with_structured_output(llm, persona)
        parsed = decision.model_dump()
    except Exception as exc:
        log.warning(f"[Node 1] Groq failed, switching to fallback mode: {exc}")
        parsed = _fallback_topic_for_persona(persona)

    log.success(f"[Node 1] Topic: '{parsed['topic']}' | Query: '{parsed['search_query']}'")

    return {"topic": parsed["topic"], "search_query": parsed["search_query"]}


def node_web_search(state: dict) -> dict:
    log.info(f"[Node 2] Searching: '{state['search_query']}'")

    search_results = mock_searxng_search.invoke({"query": state["search_query"]})

    log.success(f"[Node 2] Got results: '{search_results[:80]}...'")
    return {"search_results": search_results}


def node_draft_post(state: dict) -> dict:
    log.info("[Node 3] Drafting post...")

    persona = state["bot_persona"]
    bot_id = state["bot_id"]
    topic = state["topic"]
    search_results = state["search_results"]

    if _fallback_mode_enabled():
        parsed = _fallback_post(bot_id, topic, persona, search_results)
        log.warning("[Node 3] Fallback LLM mode active (no Groq request made)")
        log.success(f"[Node 3] Post drafted ({len(parsed['post_content'])} chars)")
        log.info(f"[Node 3] Content: {parsed['post_content']}")
        return {"final_output": parsed}

    llm = get_llm()

    try:
        parsed_model = _draft_post_with_structured_output(
            llm=llm,
            bot_id=bot_id,
            topic=topic,
            persona=persona,
            search_results=search_results,
        )
        parsed = parsed_model.model_dump()
    except Exception as exc:
        log.warning(f"[Node 3] Groq failed, switching to fallback mode: {exc}")
        parsed = _fallback_post(bot_id, topic, persona, search_results)

    if len(parsed["post_content"]) > 280:
        parsed["post_content"] = parsed["post_content"][:277] + "..."

    log.success(f"[Node 3] Post drafted ({len(parsed['post_content'])} chars)")
    log.info(f"[Node 3] Content: {parsed['post_content']}")

    return {"final_output": parsed}
