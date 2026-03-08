from __future__ import annotations

import csv
import json
from pathlib import Path

from .types import BenchmarkResult, ModelSummary


def write_results_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def write_results_csv(path: Path, results: list[BenchmarkResult]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "prompt_id",
                "model",
                "latency_ms",
                "input_tokens",
                "output_tokens",
                "total_tokens",
                "estimated_cost_usd",
                "passed",
                "score",
                "error",
            ]
        )
        for r in results:
            writer.writerow(
                [
                    r.prompt_id,
                    r.model,
                    round(r.latency_ms, 2),
                    r.usage.input_tokens,
                    r.usage.output_tokens,
                    r.usage.total_tokens,
                    r.estimated_cost_usd,
                    r.passed,
                    round(r.score, 4),
                    r.error,
                ]
            )


def write_summary_md(path: Path, summaries: list[ModelSummary]) -> None:
    lines = ["# Benchmark Summary", "", "## Ranking", ""]

    for s in summaries:
        lines.append(
            f"- **{s.model}**: quality #{s.rank_quality}, speed #{s.rank_speed}, cost #{s.rank_cost}; "
            f"avg score={s.avg_score:.3f}, pass rate={s.pass_rate:.0%}, avg latency={s.avg_latency_ms:.1f} ms, "
            f"total est. cost={'n/a' if s.total_estimated_cost_usd is None else f'${s.total_estimated_cost_usd:.6f}'}"
        )

    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
