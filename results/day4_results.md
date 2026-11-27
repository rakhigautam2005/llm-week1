# Day 4 results (gemini-3.1-flash-lite)

## Temperature 0 vs 1

| Task | Temp | Different answers | Example answer |
| --- | --- | --- | --- |
| 1 | 0.0 | 1 of 3 | Brew |
| 1 | 1.0 | 2 of 3 | Brew |
| 2 | 0.0 | 1 of 3 | 408 |
| 2 | 1.0 | 1 of 3 | 408 |
| 3 | 0.0 | 1 of 3 | $0.05 |
| 3 | 1.0 | 1 of 3 | $0.05 |
| 4 | 0.0 | 1 of 3 | Mixed |
| 4 | 1.0 | 1 of 3 | Mixed |
| 5 | 0.0 | 1 of 3 | Master the future: A beginner’s guide to understanding an... |
| 5 | 1.0 | 3 of 3 | Master the future: Your practical, no-nonsense guide to s... |

## Reasoning effort: low vs high

| Task | Effort | Output tokens | Latency (s) | Cost (USD) | Answer |
| --- | --- | --- | --- | --- | --- |
| 1 | low | 2 | 3.83 | 0.000008 | Roast |
| 1 | high | 1 | 3.55 | 0.000006 | Brew |
| 2 | low | 3 | 1.56 | 0.000009 | 408 |
| 2 | high | 3 | 5.69 | 0.000009 | 408 |
| 3 | low | 5 | 3.20 | 0.000018 | $0.05 |
| 3 | high | 5 | 5.51 | 0.000018 | $0.05 |
| 4 | low | 1 | 25.32 | 0.000008 | Mixed |
| 4 | high | 0 | 2.09 | 0.000007 | Mixed |
| 5 | low | 124 | 2.24 | 0.000189 | Here are a few options, depending on the tone you want: *... |
| 5 | high | 10 | 6.05 | 0.000018 | Unlock the power of AI—no experience required. |
