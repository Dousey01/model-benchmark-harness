from __future__ import annotations

from .types import PromptItem


def score_output(prompt: PromptItem, output: str) -> tuple[bool, float]:
    out_l = output.lower()

    checks = 0
    passed_checks = 0

    checks += 1
    if len(output.strip()) >= prompt.rubric.min_chars:
        passed_checks += 1

    for needle in prompt.rubric.must_include:
        checks += 1
        if needle.lower() in out_l:
            passed_checks += 1

    for forbidden in prompt.rubric.must_not_include:
        checks += 1
        if forbidden.lower() not in out_l:
            passed_checks += 1

    if checks == 0:
        return True, 1.0

    score = passed_checks / checks
    return score >= 0.8, score
