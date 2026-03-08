.PHONY: install test run smoke

install:
	python3 -m pip install -e .[dev]

test:
	pytest -q

run:
	mbh run --prompts benchmarks/prompts.yaml --outdir out

smoke:
	mbh run --prompts benchmarks/prompts.yaml --outdir out --max-prompts 3
