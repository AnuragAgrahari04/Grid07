from phase1.router import route_post_to_bots


def test_tech_post_routes_to_at_least_one_bot() -> None:
    result = route_post_to_bots("Elon Musk just launched a new AI chip", threshold=0.2)
    assert result.total_matched >= 1
