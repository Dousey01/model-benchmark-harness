from model_benchmark_harness.aggregate import summarize
from model_benchmark_harness.types import BenchmarkResult, Usage


def test_summarize_ranks_quality() -> None:
    results = [
        BenchmarkResult("p1", "m1", "ok", 100, Usage(), 0.1, True, 0.9),
        BenchmarkResult("p2", "m1", "ok", 120, Usage(), 0.1, True, 0.8),
        BenchmarkResult("p1", "m2", "ok", 90, Usage(), 0.2, True, 0.4),
        BenchmarkResult("p2", "m2", "ok", 95, Usage(), 0.2, False, 0.3),
    ]

    summaries = summarize(results)
    assert len(summaries) == 2
    assert summaries[0].model == "m1"
    assert summaries[0].rank_quality == 1
