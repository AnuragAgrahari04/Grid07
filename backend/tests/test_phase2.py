from phase2.engine import run_content_engine


def test_phase2_returns_post_shape() -> None:
    result = run_content_engine("bot_a")
    assert "bot_id" in result
    assert "topic" in result
    assert "post_content" in result
