"""Call an LLM and log tokens, cost and latency."""

import logging
import time

from openai import OpenAI
from pydantic import BaseModel

from llm.cost import estimate_cost

logger = logging.getLogger(__name__)


class LLMResult(BaseModel):
    text: str
    input_tokens: int
    output_tokens: int
    cost_usd: float
    latency_s: float


def ask(
    prompt: str,
    model: str,
    client: OpenAI | None = None,
    temperature: float | None = None,
    reasoning_effort: str | None = None,
) -> LLMResult:
    """Send one prompt and return the answer with its usage numbers."""
    client = client or OpenAI()  # reads OPENAI_API_KEY and OPENAI_BASE_URL from env

    options = {}  # only send settings we actually chose
    if temperature is not None:
        options["temperature"] = temperature
    if reasoning_effort is not None:
        options["reasoning_effort"] = reasoning_effort

    start = time.perf_counter()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        **options,
    )
    latency = time.perf_counter() - start

    usage = response.usage
    cost = estimate_cost(model, usage.prompt_tokens, usage.completion_tokens)
    logger.info(
        "model=%s input_tokens=%d output_tokens=%d cost_usd=%.6f latency_s=%.2f",
        model,
        usage.prompt_tokens,
        usage.completion_tokens,
        cost,
        latency,
    )
    return LLMResult(
        text=response.choices[0].message.content,
        input_tokens=usage.prompt_tokens,
        output_tokens=usage.completion_tokens,
        cost_usd=cost,
        latency_s=latency,
    )
