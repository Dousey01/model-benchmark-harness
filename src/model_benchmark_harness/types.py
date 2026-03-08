from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class Rubric:
    min_chars: int = 0
    must_include: list[str] = field(default_factory=list)
    must_not_include: list[str] = field(default_factory=list)


@dataclass(slots=True)
class PromptItem:
    id: str
    category: str
    text: str
    rubric: Rubric = field(default_factory=Rubric)


@dataclass(slots=True)
class Usage:
    input_tokens: int | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None


@dataclass(slots=True)
class BenchmarkResult:
    prompt_id: str
    model: str
    output: str
    latency_ms: float
    usage: Usage
    estimated_cost_usd: float | None
    passed: bool
    score: float
    error: str | None = None


@dataclass(slots=True)
class ModelSummary:
    model: str
    avg_latency_ms: float
    avg_score: float
    pass_rate: float
    total_estimated_cost_usd: float | None
    rank_quality: int = 0
    rank_speed: int = 0
    rank_cost: int = 0


JSONDict = dict[str, Any]
