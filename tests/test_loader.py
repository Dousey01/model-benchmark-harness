from model_benchmark_harness.loader import load_prompts


def test_load_prompts_yaml() -> None:
    prompts = load_prompts("benchmarks/prompts.yaml")
    assert len(prompts) >= 15
    assert prompts[0].id
    assert prompts[0].category
    assert prompts[0].text


def test_load_prompts_has_rubric_defaults() -> None:
    prompts = load_prompts("benchmarks/prompts.yaml")
    item = prompts[0]
    assert item.rubric.min_chars >= 0
    assert isinstance(item.rubric.must_include, list)
    assert isinstance(item.rubric.must_not_include, list)
