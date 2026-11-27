"""Day 4 experiments: temperature 0 vs 1, and low vs high reasoning effort."""

import logging
import os
import time
from pathlib import Path

from dotenv import load_dotenv

from llm.client import ask

logger = logging.getLogger(__name__)

TASKS = [
    "Suggest a one-word name for a coffee shop. Reply with the name only.",
    "What is 17 * 24? Reply with the number only.",
    "A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the ball. "
    "How much does the ball cost? Reply with the amount only.",
    "Is the sentiment of 'The delivery was late but the food was great' positive, "
    "negative or mixed? Reply with one word.",
    "Write a one-line tagline for an AI course for beginners.",
]


def short(text: str, limit: int = 60) -> str:
    """One line, cut to a readable length, safe for a markdown table."""
    one_line = " ".join(text.split()).replace("|", "/")
    return one_line if len(one_line) <= limit else one_line[: limit - 3] + "..."


def count_distinct(answers: list[str]) -> int:
    """How many different answers, ignoring case and extra spaces."""
    return len({" ".join(a.lower().split()) for a in answers})


def temperature_test(model: str, runs: int, pause: float) -> list[str]:
    rows = ["| Task | Temp | Different answers | Example answer |", "| --- | --- | --- | --- |"]
    for i, task in enumerate(TASKS, start=1):
        for temperature in (0.0, 1.0):
            answers = []
            for _ in range(runs):
                answers.append(ask(task, model, temperature=temperature).text)
                time.sleep(pause)
            distinct = count_distinct(answers)
            rows.append(f"| {i} | {temperature} | {distinct} of {runs} | {short(answers[0])} |")
    return rows


def reasoning_test(model: str, efforts: tuple[str, str], pause: float) -> list[str]:
    rows = [
        "| Task | Effort | Output tokens | Latency (s) | Cost (USD) | Answer |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for i, task in enumerate(TASKS, start=1):
        for effort in efforts:
            result = ask(task, model, reasoning_effort=effort)
            rows.append(
                f"| {i} | {effort} | {result.output_tokens} | {result.latency_s:.2f} "
                f"| {result.cost_usd:.6f} | {short(result.text)} |"
            )
            time.sleep(pause)
    return rows


def run() -> None:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
    )
    load_dotenv()
    model = os.getenv("LLM_MODEL", "gpt-4o-mini")
    pause = float(os.getenv("PAUSE_S", "2"))  # wait between calls to respect rate limits

    lines = [f"# Day 4 results ({model})", "", "## Temperature 0 vs 1", ""]
    lines += temperature_test(model, runs=3, pause=pause)
    lines += ["", "## Reasoning effort: low vs high", ""]
    lines += reasoning_test(model, efforts=("low", "high"), pause=pause)

    out = Path("results/day4_results.md")
    out.parent.mkdir(exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    logger.info("Saved %s", out)


if __name__ == "__main__":
    run()
