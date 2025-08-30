from __future__ import annotations

from .metrics import (
    estimate_cost,
    run_accuracy,
    run_fairness,
    run_hallucination,
    run_latency,
    write_run_log,
)
from .models import ModelResponse, StubModel
from .paths import DATA_DIR, REPORTS_DIR, ensure_reports_dir


def main() -> None:
    ensure_reports_dir()

    model = StubModel(answers_path=DATA_DIR / "answers.json")

    acc = run_accuracy(model)
    lat = run_latency(model)
    fai = run_fairness(model)
    hal = run_hallucination(model)

    total_in = acc["tokens_in"]
    total_out = acc["tokens_out"]
    cost = estimate_cost(total_in, total_out)

    entries = []
    for item in acc["items"]:
        resp = ModelResponse(
            text=item["got"],
            tokens_in=item["tokens_in"],
            tokens_out=item["tokens_out"],
            latency_ms=item["latency_ms"],
        )
        entries.append((item["prompt"], resp))
    write_run_log(entries)

    summary = (
        "# Benchmark Summary\n\n"
        f"- **Accuracy:** {acc['accuracy']:.2%} on {acc['n']} items\n"
        f"- **Avg Latency:** {lat['avg_latency_ms']:.2f} ms "
        f"(p95: {lat['p95_latency_ms']:.2f} ms) on {lat['n']} runs\n"
        f"- **Fairness (African langs):** per-language accuracy = "
        f"{fai['per_language_accuracy']}, gap = {fai['fairness_gap']:.2%}\n"
        f"- **Hallucination Risk:** average risk = {hal['avg_risk']:.2f} "
        f"(0 best, 1 worst) over {hal['n']} checks\n"
        f"- **Cost (toy estimate):** ${cost['usd']} for accuracy run "
        f"(rates: {cost['rates_per_1k']})\n"
    )

    (REPORTS_DIR / "summary.md").write_text(summary, encoding="utf-8")


if __name__ == "__main__":
    main()
