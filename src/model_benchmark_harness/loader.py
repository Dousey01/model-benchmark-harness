from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from .types import PromptItem, Rubric


def _coerce_rubric(raw: dict[str, Any] | None) -> Rubric:
    raw = raw or {}
    return Rubric(
        min_chars=int(raw.get("min_chars", 0)),
        must_include=list(raw.get("must_include", [])),
        must_not_include=list(raw.get("must_not_include", [])),
    )


def load_prompts(path: str | Path) -> list[PromptItem]:
    p = Path(path)
    text = p.read_text(encoding="utf-8")

    if p.suffix.lower() in {".yaml", ".yml"}:
        data = yaml.safe_load(text)
    elif p.suffix.lower() == ".json":
        data = json.loads(text)
    else:
        raise ValueError(f"Unsupported prompt file extension: {p.suffix}")

    if not isinstance(data, dict) or "prompts" not in data:
        raise ValueError("Prompt file must be an object with a 'prompts' array")

    items: list[PromptItem] = []
    for raw in data["prompts"]:
        items.append(
            PromptItem(
                id=str(raw["id"]),
                category=str(raw["category"]),
                text=str(raw["text"]),
                rubric=_coerce_rubric(raw.get("rubric")),
            )
        )
    return items
