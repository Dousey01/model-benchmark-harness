# model-benchmark-harness

CLI-first Python harness to compare local vs cloud model performance across quality, latency, and estimated cost.

## Models (default)
- `openai-codex/gpt-5.3-codex`
- `anthropic/claude-sonnet-4-6`
- `anthropic/claude-opus-4-6`
- `local/qwen2.5:1.5b` (Ollama-compatible OpenAI API at `http://localhost:11434`)

## Requirements
- Python 3.11+
- `OPENROUTER_API_KEY` for cloud models
- Ollama running locally for `local/qwen2.5:1.5b`

## One-command run
```bash
make run
```

## Install + test
```bash
make install
make test
```

## Smoke benchmark (3 prompts)
```bash
make smoke
```

## Offline smoke (deterministic mock mode)
```bash
make smoke-offline
```
Use this in CI or when APIs/local model runtimes are unavailable.

## CLI
```bash
mbh \
  --prompts benchmarks/prompts.yaml \
  --outdir out \
  --models openai-codex/gpt-5.3-codex,local/qwen2.5:1.5b \
  --max-prompts 3 \
  --timeout-s 45 \
  --retries 2 \
  --offline
```

## Outputs
- `results.json` - full per-prompt/per-model records (raw output, latency, usage, est. cost, pass/fail, score)
- `results.csv` - flat export
- `summary.md` - model ranking by quality/speed/cost

## Notes
- Cost estimates are approximate token-price calculations from static defaults in `pricing.py`.
- Token usage depends on provider response fields; missing usage is handled gracefully.
