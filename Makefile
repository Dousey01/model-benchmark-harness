.PHONY: install test run smoke

install:
	python3 -m pip install -e .[dev]

test:
	pytest -q

run:
	mbh --prompts benchmarks/prompts.yaml --outdir out

smoke:
	mbh --prompts benchmarks/prompts.yaml --outdir out --max-prompts 3
