from model_benchmark_harness.scoring import score_output
from model_benchmark_harness.types import PromptItem, Rubric


def test_score_output_supports_alternatives() -> None:
    prompt = PromptItem(
        id="x",
        category="test",
        text="t",
        rubric=Rubric(min_chars=5, must_include=["join|append"]),
    )
    passed, score = score_output(prompt, "Use append in a loop")
    assert passed
    assert score >= 0.75
