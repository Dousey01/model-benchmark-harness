from __future__ import annotations

from collections import defaultdict

from .types import BenchmarkResult, ModelSummary


def summarize(results: list[BenchmarkResult]) -> list[ModelSummary]:
    grouped: dict[str, list[BenchmarkResult]] = defaultdict(list)
    for r in results:
        grouped[r.model].append(r)

    summaries: list[ModelSummary] = []
    for model, items in grouped.items():
        avg_latency = sum(i.latency_ms for i in items) / len(items)
        avg_score = sum(i.score for i in items) / len(items)
        pass_rate = sum(1 for i in items if i.passed) / len(items)

        costs = [i.estimated_cost_usd for i in items if i.estimated_cost_usd is not None]
        total_cost = sum(costs) if costs else None

        summaries.append(
            ModelSummary(
                model=model,
                avg_latency_ms=avg_latency,
                avg_score=avg_score,
                pass_rate=pass_rate,
                total_estimated_cost_usd=total_cost,
            )
        )

    by_quality = sorted(summaries, key=lambda s: s.avg_score, reverse=True)
    by_speed = sorted(summaries, key=lambda s: s.avg_latency_ms)
    by_cost = sorted(
        summaries,
        key=lambda s: float("inf") if s.total_estimated_cost_usd is None else s.total_estimated_cost_usd,
    )

    for i, s in enumerate(by_quality, 1):
        s.rank_quality = i
    for i, s in enumerate(by_speed, 1):
        s.rank_speed = i
    for i, s in enumerate(by_cost, 1):
        s.rank_cost = i

    return sorted(summaries, key=lambda s: s.rank_quality)
