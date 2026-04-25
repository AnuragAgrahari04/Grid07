"""
LangGraph state machine for Phase 2.
Graph structure:
  START -> decide_search -> web_search -> draft_post -> END
"""

from typing import Optional, TypedDict

from langgraph.graph import END, START, StateGraph

from core.logger import log
from phase2.nodes import node_decide_search, node_draft_post, node_web_search


class GraphState(TypedDict):
    bot_id: str
    bot_persona: str
    topic: Optional[str]
    search_query: Optional[str]
    search_results: Optional[str]
    final_output: Optional[dict]


def build_content_graph() -> StateGraph:
    graph = StateGraph(GraphState)

    graph.add_node("decide_search", node_decide_search)
    graph.add_node("web_search", node_web_search)
    graph.add_node("draft_post", node_draft_post)

    graph.add_edge(START, "decide_search")
    graph.add_edge("decide_search", "web_search")
    graph.add_edge("web_search", "draft_post")
    graph.add_edge("draft_post", END)

    return graph.compile()


CONTENT_GRAPH = build_content_graph()


def run_graph(bot_id: str, bot_persona: str) -> dict:
    log.info(f"Running content engine graph for {bot_id}...")

    initial_state: GraphState = {
        "bot_id": bot_id,
        "bot_persona": bot_persona,
        "topic": None,
        "search_query": None,
        "search_results": None,
        "final_output": None,
    }

    final_state = CONTENT_GRAPH.invoke(initial_state)
    log.success(f"Content engine graph complete for {bot_id}")
    return final_state["final_output"]
