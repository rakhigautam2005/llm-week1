"""Stream an LLM answer piece by piece and measure time to first token."""

import logging
import os
import sys
import time
from collections.abc import Iterator

from dotenv import load_dotenv
from openai import OpenAI

from llm.cost import estimate_cost

logger = logging.getLogger(__name__)


def stream_answer(prompt: str, model: str, client: OpenAI | None = None) -> Iterator[str]:
    """Yield text pieces as they arrive. Log speed, tokens and cost at the end."""
    client = client or OpenAI()
    start = time.perf_counter()
    ttft = None  # time to first token
    usage = None

    stream = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
        stream_options={"include_usage": True},  # ask for token counts in the last chunk
    )
    for chunk in stream:
        if getattr(chunk, "usage", None):
            usage = chunk.usage
        if chunk.choices and chunk.choices[0].delta.content:
            if ttft is None:
                ttft = time.perf_counter() - start
            yield chunk.choices[0].delta.content

    latency = time.perf_counter() - start
    if usage:
        cost = estimate_cost(model, usage.prompt_tokens, usage.completion_tokens)
        logger.info(
            "model=%s ttft_s=%.2f latency_s=%.2f input_tokens=%d output_tokens=%d cost_usd=%.6f",
            model,
            ttft or 0.0,
            latency,
            usage.prompt_tokens,
            usage.completion_tokens,
            cost,
        )
    else:
        logger.info(
            "model=%s ttft_s=%.2f latency_s=%.2f (no usage reported)", model, ttft or 0.0, latency
        )


def run() -> None:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
    )
    load_dotenv()
    model = os.getenv("LLM_MODEL", "gpt-4o-mini")
    prompt = " ".join(sys.argv[1:]) or "Explain what an LLM is in 5 short sentences."

    for piece in stream_answer(prompt, model):
        print(piece, end="", flush=True)
    print()


if __name__ == "__main__":
    run()
