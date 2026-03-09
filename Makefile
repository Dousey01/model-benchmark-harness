.PHONY: install test run smoke smoke-offline

install:
	python3 -m pip install -e .[dev]

test:
	pytest -q

run:
	mbh --prompts benchmarks/prompts.yaml --outdir out

smoke:
	mbh --prompts benchmarks/prompts.yaml --outdir out --max-prompts 3

smoke-offline:
	mbh --prompts benchmarks/prompts.yaml --outdir out --max-prompts 3 --offline
