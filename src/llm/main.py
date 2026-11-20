"""Command line: ask the LLM one question."""

import logging
import os
import sys

from dotenv import load_dotenv

from llm.client import ask


def run() -> None:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
    )
    load_dotenv()
    model = os.getenv("LLM_MODEL", "gpt-4o-mini")
    prompt = " ".join(sys.argv[1:]) or "Explain what a token is in one sentence."

    result = ask(prompt, model)
    print(result.text)


if __name__ == "__main__":
    run()
