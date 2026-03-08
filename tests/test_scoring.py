from model_benchmark_harness.scoring import score_output
from model_benchmark_harness.types import PromptItem, Rubric


def test_score_output_pass() -> None:
    prompt = PromptItem(
        id="x",
        category="test",
        text="t",
        rubric=Rubric(min_chars=10, must_include=["hello"], must_not_include=["forbidden"]),
    )
    passed, score = score_output(prompt, "hello world, this passes")
    assert passed
    assert score >= 0.8


def test_score_output_fail() -> None:
    prompt = PromptItem(
        id="x",
        category="test",
        text="t",
        rubric=Rubric(min_chars=20, must_include=["hello", "python"]),
    )
    passed, score = score_output(prompt, "hello")
    assert not passed
    assert score < 0.8
