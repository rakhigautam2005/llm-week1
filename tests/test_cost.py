import pytest

from llm.cost import estimate_cost


def test_cost_math():
    # 1M input tokens at $0.15 + 1M output tokens at $0.60 = $0.75
    assert estimate_cost("gpt-4o-mini", 1_000_000, 1_000_000) == pytest.approx(0.75)


def test_small_call_is_cheap():
    cost = estimate_cost("gpt-4o-mini", 100, 50)
    assert cost == pytest.approx(0.000045)


def test_unknown_model_raises():
    with pytest.raises(ValueError):
        estimate_cost("made-up-model", 10, 10)
