import asyncio

from model_benchmark_harness.loader import load_prompts
from model_benchmark_harness.runner import run_benchmark


def test_offline_mode_returns_results_without_network() -> None:
    prompts = load_prompts("benchmarks/prompts.yaml")[:1]
    models = ["openai-codex/gpt-5.3-codex", "local/qwen2.5:1.5b"]

    results = asyncio.run(run_benchmark(prompts, models, timeout_s=1.0, retries=0, offline=True))

    assert len(results) == 2
    assert all(r.error is None for r in results)
    assert all("OFFLINE_MOCK" in r.output for r in results)
    assert all(r.latency_ms > 0 for r in results)
