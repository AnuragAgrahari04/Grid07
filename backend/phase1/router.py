"""
Phase 1 - Core routing function.
Main deliverable: route_post_to_bots().
"""

from core.logger import log
from core.models import BotMatch, RoutingResult
from personas.bots import BOTS_BY_ID
from phase1.vector_store import query_similar_bots


def route_post_to_bots(post_content: str, threshold: float = 0.85) -> RoutingResult:

    log.info(f"Routing post: '{post_content[:60]}...' (threshold={threshold})")

    all_results = query_similar_bots(post_content, n_results=3)

    matched = []
    for result in all_results:
        bot_id = result["bot_id"]
        similarity = result["similarity"]
        persona = BOTS_BY_ID.get(bot_id)

        status = "MATCH" if similarity >= threshold else "below-threshold"
        log.info(f"  {bot_id}: similarity={similarity:.4f} {status}")

        if similarity >= threshold:
            matched.append(
                BotMatch(
                    bot_id=bot_id,
                    bot_name=persona.name if persona else bot_id,
                    similarity_score=similarity,
                    will_respond=True,
                )
            )

    log.success(f"Routing complete. {len(matched)}/{len(all_results)} bots matched.")

    return RoutingResult(
        post_content=post_content,
        threshold_used=threshold,
        all_scores=[
            BotMatch(
                bot_id=r["bot_id"],
                bot_name=BOTS_BY_ID[r["bot_id"]].name if r["bot_id"] in BOTS_BY_ID else r["bot_id"],
                similarity_score=r["similarity"],
                will_respond=r["similarity"] >= threshold,
            )
            for r in all_results
        ],
        matched_bots=matched,
        total_matched=len(matched),
    )
