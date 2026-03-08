from __future__ import annotations

from .types import Usage

# USD per 1M tokens (approximate, configurable in code for v1)
PRICE_TABLE: dict[str, tuple[float, float]] = {
    "openai-codex/gpt-5.3-codex": (1.50, 6.00),
    "anthropic/claude-sonnet-4-6": (3.00, 15.00),
    "anthropic/claude-opus-4-6": (15.00, 75.00),
    "local/qwen2.5:1.5b": (0.0, 0.0),
}


def estimate_cost_usd(model: str, usage: Usage) -> float | None:
    if model not in PRICE_TABLE:
        return None
    in_price, out_price = PRICE_TABLE[model]

    if usage.input_tokens is None and usage.output_tokens is None:
        return None

    in_tokens = usage.input_tokens or 0
    out_tokens = usage.output_tokens or 0

    return (in_tokens / 1_000_000) * in_price + (out_tokens / 1_000_000) * out_price
