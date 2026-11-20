# llm-week1

Week 1 of my AI engineering plan: tokens, cost, and my first LLM calls.

## What's inside

- `notebooks/tokens_and_cost.ipynb`: counts tokens and estimates cost for 5 prompts. Compares English vs Hindi, and an old vs new tokenizer.
- `src/llm/cost.py`: price table and cost formula per model
- `src/llm/client.py`: calls an LLM and logs input tokens, output tokens, cost and latency
- `src/llm/main.py`: command line entry point

## Key findings

- Hindi used 1.3x the tokens of English with the new o200k tokenizer, but 3.3x with the older cl100k tokenizer.
- Output tokens are priced several times higher than input, so answer length drives cost.

## Setup

```bash
uv sync
cp .env.example .env   # then add your API key
```

Works with OpenAI, or with Google Gemini through its OpenAI-compatible endpoint. Switch providers by editing `.env` only.

## Run

```bash
uv run python -m llm.main "What is a token? Answer in one sentence."
```

Example log line:

```
model=gemini-3.1-flash-lite input_tokens=11 output_tokens=36 cost_usd=0.000057 latency_s=26.80
```

## Test

```bash
uv run python -m pytest -v
```

4 tests. The LLM client is tested with a fake client, so tests run offline and cost nothing.