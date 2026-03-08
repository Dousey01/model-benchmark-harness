from __future__ import annotations

import asyncio
from pathlib import Path

import typer

from .aggregate import summarize
from .loader import load_prompts
from .report import write_results_csv, write_results_json, write_summary_md
from .runner import results_to_jsonable, run_benchmark

DEFAULT_MODELS = [
    "openai-codex/gpt-5.3-codex",
    "anthropic/claude-sonnet-4-6",
    "anthropic/claude-opus-4-6",
    "local/qwen2.5:1.5b",
]

app = typer.Typer(help="Local-vs-cloud model benchmark harness")


@app.command()
def run(
    prompts: str = typer.Option(..., help="Path to prompts YAML/JSON"),
    outdir: str = typer.Option("out", help="Output directory"),
    models: str = typer.Option("", help="Comma-separated model filter"),
    max_prompts: int = typer.Option(0, help="Max number of prompts to run"),
    timeout_s: float = typer.Option(60.0, help="Per-call timeout seconds"),
    retries: int = typer.Option(2, help="Retries per call"),
) -> None:
    prompt_items = load_prompts(prompts)
    if max_prompts > 0:
        prompt_items = prompt_items[:max_prompts]

    model_list = [m.strip() for m in models.split(",") if m.strip()] if models else DEFAULT_MODELS

    results = asyncio.run(run_benchmark(prompt_items, model_list, timeout_s=timeout_s, retries=retries))
    summaries = summarize(results)

    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)

    write_results_json(
        out / "results.json",
        {
            "models": model_list,
            "prompt_count": len(prompt_items),
            "results": results_to_jsonable(results),
            "summaries": [s.__dict__ for s in summaries],
        },
    )
    write_results_csv(out / "results.csv", results)
    write_summary_md(out / "summary.md", summaries)

    typer.echo(f"Wrote: {out / 'results.json'}")
    typer.echo(f"Wrote: {out / 'results.csv'}")
    typer.echo(f"Wrote: {out / 'summary.md'}")


if __name__ == "__main__":
    app()
