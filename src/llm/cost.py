"""Token prices and cost math."""

# USD per 1 million tokens. Prices change: check the provider's pricing page.
PRICES: dict[str, dict[str, float]] = {
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gemini-3.1-flash-lite": {"input": 0.25, "output": 1.50},
}


def estimate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """Return the cost in USD for one call."""
    if model not in PRICES:
        raise ValueError(f"No price for model {model!r}. Add it to PRICES.")
    price = PRICES[model]
    return (input_tokens * price["input"] + output_tokens * price["output"]) / 1_000_000
