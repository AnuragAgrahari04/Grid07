"""
Pydantic data models for the entire project.
Defines input/output shapes for all three phases.
"""

from typing import Optional

from pydantic import BaseModel, Field


class RouteRequest(BaseModel):
    post_content: str = Field(..., description="The social media post to route")
    threshold: Optional[float] = Field(None, description="Cosine similarity threshold (0-1)")


class BotMatch(BaseModel):
    bot_id: str
    bot_name: str
    similarity_score: float
    will_respond: bool


class RoutingResult(BaseModel):
    post_content: str
    threshold_used: float
    all_scores: list[BotMatch]
    matched_bots: list[BotMatch]
    total_matched: int


class GenerateRequest(BaseModel):
    bot_id: str = Field(..., description="Which bot generates the post: bot_a, bot_b, bot_c")


class PostOutput(BaseModel):
    bot_id: str
    topic: str
    post_content: str


class ThreadMessage(BaseModel):
    author: str
    content: str
    is_bot: bool = False


class CombatRequest(BaseModel):
    bot_id: str
    parent_post: str
    comment_history: list[ThreadMessage]
    human_reply: str


class CombatResult(BaseModel):
    bot_id: str
    bot_name: str
    reply: str
    injection_detected: bool
    thread_depth: int
