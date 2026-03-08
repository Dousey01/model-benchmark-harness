from __future__ import annotations

import re

from .types import PromptItem


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9+.#_\-\s]", " ", text.lower())).strip()


def _contains_with_alternatives(haystack: str, expression: str) -> bool:
    """Allow simple alternatives in rubric values, e.g. 'join|append'."""
    options = [opt.strip() for opt in expression.split("|") if opt.strip()]
    if not options:
        return False
    return any(_normalize(opt) in haystack for opt in options)


def score_output(prompt: PromptItem, output: str) -> tuple[bool, float]:
    out_n = _normalize(output)

    checks = 0
    passed_checks = 0

    checks += 1
    if len(output.strip()) >= prompt.rubric.min_chars:
        passed_checks += 1

    for needle in prompt.rubric.must_include:
        checks += 1
        if _contains_with_alternatives(out_n, needle):
            passed_checks += 1

    for forbidden in prompt.rubric.must_not_include:
        checks += 1
        if not _contains_with_alternatives(out_n, forbidden):
            passed_checks += 1

    if checks == 0:
        return True, 1.0

    score = passed_checks / checks

    # Slightly gentler pass gate when rubric has very few checks.
    pass_threshold = 0.75 if checks <= 3 else 0.8
    return score >= pass_threshold, score
