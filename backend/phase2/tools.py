"""
Mock search tool for Phase 2.
In production, this would call SearXNG or another search API.
"""

from langchain_core.tools import tool

from core.logger import log

MOCK_NEWS = {
    "crypto": (
        "Bitcoin hits new all-time high amid regulatory ETF approvals. "
        "Institutional investors pour $2.3B into crypto funds this week."
    ),
    "bitcoin": (
        "Bitcoin surpasses $100K milestone. MicroStrategy adds 10,000 BTC to treasury. "
        "Wall Street analysts revise price targets upward."
    ),
    "ai": (
        "OpenAI releases GPT-5 with 10x reasoning improvements. "
        "Tech giants race to deploy AI agents. 40% of junior coding tasks now automated."
    ),
    "openai": (
        "OpenAI valued at $300B after latest funding round. "
        "New model outperforms human experts on medical and legal benchmarks."
    ),
    "tesla": (
        "Tesla FSD achieves Level 4 autonomy in 12 US cities. "
        "Robotaxi fleet generates $500M revenue in Q3."
    ),
    "elon": (
        "Elon Musk announces xAI partnership with SpaceX for satellite-based AI inference. "
        "Grok 3 beats competitors on reasoning benchmarks."
    ),
    "regulation": (
        "EU AI Act enforcement begins. 23 companies face compliance audits. "
        "US Senate passes landmark AI liability bill with bipartisan support."
    ),
    "surveillance": (
        "Leaked documents reveal major social platforms sold location data to governments. "
        "Privacy advocates call for immediate antitrust action against Big Tech."
    ),
    "climate": (
        "UN report: Tech industry carbon footprint doubled since 2020. "
        "AI data centers consume more electricity than medium-sized countries."
    ),
    "market": (
        "S&P 500 hits record high on strong earnings. "
        "Fed signals two rate cuts in 2025. Tech sector leads gains with 4.2% rally."
    ),
    "fed": (
        "Federal Reserve holds rates steady at 4.25-4.50%. "
        "Powell signals data-dependent approach. Yield curve inverts further."
    ),
    "interest": (
        "10-year Treasury yield drops to 3.8% on weak jobs data. "
        "Mortgage rates fall to 18-month low. Housing market shows signs of recovery."
    ),
    "stock": (
        "Nvidia Q4 earnings beat expectations by 23%. "
        "Options market pricing in 15% volatility for earnings week. "
        "Short interest at multi-year low."
    ),
    "ev": (
        "EV sales hit 18% of all new car sales globally. "
        "Battery costs drop to $78/kWh. Range anxiety cited as top remaining barrier."
    ),
    "space": (
        "SpaceX Starship completes 8th test flight with full payload. "
        "NASA confirms Moon mission on track for 2026 using Starship."
    ),
}

DEFAULT_NEWS = (
    "Tech stocks mixed as investors weigh AI optimism against macro headwinds. "
    "Volatility index rises ahead of Fed meeting. "
    "Big Tech earnings season begins next week."
)


@tool
def mock_searxng_search(query: str) -> str:
    """
    Search for recent news headlines relevant to the query.
    Returns a string of recent headlines and brief summaries.
    """
    log.info(f"[mock_searxng_search] Query: '{query}'")

    query_lower = query.lower()

    found_results = []
    for keyword, headline in MOCK_NEWS.items():
        if keyword in query_lower:
            found_results.append(headline)
            if len(found_results) >= 2:
                break

    result = " | ".join(found_results) if found_results else DEFAULT_NEWS

    log.info(f"[mock_searxng_search] Result: '{result[:80]}...'")
    return result
