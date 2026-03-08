from __future__ import annotations

import asyncio
import time
from dataclasses import asdict

import httpx

from .pricing import estimate_cost_usd
from .scoring import score_output
from .types import BenchmarkResult, PromptItem, Usage


class ModelClient:
    def __init__(self, timeout_s: float = 60.0, retries: int = 2) -> None:
        self.timeout_s = timeout_s
        self.retries = retries

    async def call_model(self, model: str, prompt: str) -> tuple[str, Usage, float, str | None]:
        start = time.perf_counter()
        error: str | None = None

        if model.startswith("local/"):
            api_url = "http://localhost:11434/v1/chat/completions"
            real_model = model.split("/", 1)[1]
            headers: dict[str, str] = {"Content-Type": "application/json"}
        else:
            api_url = "https://openrouter.ai/api/v1/chat/completions"
            real_model = model
            import os

            api_key = os.getenv("OPENROUTER_API_KEY", "")
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }

        payload = {
            "model": real_model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
        }

        for attempt in range(self.retries + 1):
            try:
                async with httpx.AsyncClient(timeout=self.timeout_s) as client:
                    resp = await client.post(api_url, headers=headers, json=payload)
                    resp.raise_for_status()
                    data = resp.json()

                text = data["choices"][0]["message"]["content"]
                usage_raw = data.get("usage", {}) or {}
                usage = Usage(
                    input_tokens=usage_raw.get("prompt_tokens") or usage_raw.get("input_tokens"),
                    output_tokens=usage_raw.get("completion_tokens") or usage_raw.get("output_tokens"),
                    total_tokens=usage_raw.get("total_tokens"),
                )
                latency_ms = (time.perf_counter() - start) * 1000
                return text, usage, latency_ms, None
            except Exception as exc:  # noqa: BLE001
                error = str(exc)
                if attempt < self.retries:
                    await asyncio.sleep(0.6 * (attempt + 1))
                else:
                    break

        latency_ms = (time.perf_counter() - start) * 1000
        return "", Usage(), latency_ms, error


async def run_benchmark(prompts: list[PromptItem], models: list[str], timeout_s: float, retries: int) -> list[BenchmarkResult]:
    client = ModelClient(timeout_s=timeout_s, retries=retries)
    results: list[BenchmarkResult] = []

    for prompt in prompts:
        for model in models:
            out, usage, latency_ms, error = await client.call_model(model=model, prompt=prompt.text)
            passed, score = score_output(prompt, out)
            cost = estimate_cost_usd(model, usage)
            results.append(
                BenchmarkResult(
                    prompt_id=prompt.id,
                    model=model,
                    output=out,
                    latency_ms=latency_ms,
                    usage=usage,
                    estimated_cost_usd=cost,
                    passed=passed and error is None,
                    score=0.0 if error else score,
                    error=error,
                )
            )

    return results


def results_to_jsonable(results: list[BenchmarkResult]) -> list[dict]:
    out: list[dict] = []
    for r in results:
        item = asdict(r)
        item["usage"] = asdict(r.usage)
        out.append(item)
    return out
