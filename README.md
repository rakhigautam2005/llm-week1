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
## Day 4: Streaming, temperature and reasoning effort

- `src/llm/stream.py`: streams the answer piece by piece and logs time to first token (TTFT) and total latency separately
- `src/llm/compare.py`: runs 5 tasks at temperature 0 vs 1 (3 runs each) and at low vs high reasoning effort, then saves a table to `results/day4_results.md`

```bash
uv run python -m llm.stream "Write 10 short tips for learning Python, one per line."
uv run python -m llm.compare
```

### Findings (gemini-3.1-flash-lite, free tier)

- Temperature only added variety on creative tasks: the tagline gave 3 different answers out of 3 at temperature 1, but 1 at temperature 0. Maths, logic and classification gave the same correct answer at both.
- Low and high reasoning effort both solved every task, including the bat and ball trap ($0.05). High effort was usually slower (17 x 24: 1.56 s vs 5.69 s).
- On the tagline task, low effort ignored "one line" and returned several options (124 tokens). High effort followed the instruction (10 tokens), so it was 10x cheaper there.
- Thinking tokens were not reported in output tokens through the OpenAI-compatible endpoint, so their cost could not be measured directly.
- Latency was noisy on the free tier (one call took 25 s, similar calls took 2 s). TTFT logs showed the delay was queue time before the first token, not generation. A fair speed comparison needs several runs and the median.