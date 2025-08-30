from __future__ import annotations

import csv
import json
import statistics
from typing import Dict, List, Tuple

from .models import BaseModel, ModelResponse
from .paths import DATA_DIR, REPORTS_DIR, ensure_reports_dir


def _normalize(s: str) -> str:
    return " ".join(s.strip().lower().split())


def _read_csv(path):
    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def _write_json(path, payload: dict) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def run_accuracy(model: BaseModel) -> dict:
    """Exact(ish) match on toy QA set."""
    rows = _read_csv(DATA_DIR / "prompts.csv")
    total = len(rows)
    correct = 0
    per_item: List[dict] = []

    tokens_in_sum = 0
    tokens_out_sum = 0
    latencies: List[float] = []

    for r in rows:
        prompt = r["prompt"]
        expected = r["expected"]
        resp: ModelResponse = model.generate(prompt)
        ok = _normalize(resp.text) == _normalize(expected)
        correct += int(ok)
        per_item.append(
            {
                "id": r["id"],
                "prompt": prompt,
                "expected": expected,
                "got": resp.text,
                "pass": bool(ok),
                "latency_ms": round(resp.latency_ms, 3),
                "tokens_in": resp.tokens_in,
                "tokens_out": resp.tokens_out,
            }
        )
        tokens_in_sum += resp.tokens_in
        tokens_out_sum += resp.tokens_out
        latencies.append(resp.latency_ms)

    result = {
        "accuracy": correct / total if total else 0.0,
        "n": total,
        "avg_latency_ms": statistics.fmean(latencies) if latencies else 0.0,
        "tokens_in": tokens_in_sum,
        "tokens_out": tokens_out_sum,
        "items": per_item,
    }

    ensure_reports_dir()
    _write_json(REPORTS_DIR / "accuracy.json", result)
    return result


def run_latency(model: BaseModel) -> dict:
    """Simple average latency across the same QA set."""
    rows = _read_csv(DATA_DIR / "prompts.csv")
    latencies = []
    for r in rows:
        resp = model.generate(r["prompt"])
        latencies.append(resp.latency_ms)

    p95 = (
        sorted(latencies)[int(0.95 * (len(latencies) - 1))]
        if latencies
        else 0.0
    )

    result = {
        "avg_latency_ms": statistics.fmean(latencies) if latencies else 0.0,
        "p95_latency_ms": p95,
        "n": len(latencies),
    }
    ensure_reports_dir()
    _write_json(REPORTS_DIR / "latency.json", result)
    return result


def run_fairness(model: BaseModel) -> dict:
    """Per-language accuracy for African languages (toy)."""
    rows = _read_csv(DATA_DIR / "fairness.csv")
    lang_stats: Dict[str, List[bool]] = {}

    for r in rows:
        lang = r["language"]
        resp = model.generate(r["prompt"])
        ok = _normalize(resp.text) == _normalize(r["expected"])
        lang_stats.setdefault(lang, []).append(ok)

    accuracies = {k: (sum(map(int, v)) / len(v)) for k, v in lang_stats.items()}
    fairness_gap = (max(accuracies.values()) - min(accuracies.values())) if accuracies else 0.0
    result = {"per_language_accuracy": accuracies, "fairness_gap": fairness_gap, "n": len(rows)}

    ensure_reports_dir()
    _write_json(REPORTS_DIR / "fairness.json", result)
    return result


def run_hallucination(model: BaseModel) -> dict:
    """
    Toy 'source-grounding':
    Risk = 0 if model output contains the required source string (or an expected marker),
    else 1. Lower is better.
    """
    rows = _read_csv(DATA_DIR / "claims.csv")
    risks = []
    details = []
    for r in rows:
        prompt = r["prompt"]
        source = r["source"]
        expect_contains = r["expected_contains"]
        resp = model.generate(prompt)
        grounded = (source in resp.text) or (expect_contains in resp.text)
        risk = 0 if grounded else 1
        risks.append(risk)
        details.append(
            {
                "id": r["id"],
                "prompt": prompt,
                "source_required": source,
                "expected_contains": expect_contains,
                "got": resp.text,
                "risk": risk,
            }
        )

    result = {
        "avg_risk": statistics.fmean(risks) if risks else 0.0,
        "items": details,
        "n": len(rows),
    }

    ensure_reports_dir()
    _write_json(REPORTS_DIR / "hallucination.json", result)
    return result


def write_run_log(entries: List[Tuple[str, ModelResponse]]) -> None:
    ensure_reports_dir()
    path = REPORTS_DIR / "run_log.csv"
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["prompt", "output", "latency_ms", "tokens_in", "tokens_out"])
        for prompt, resp in entries:
            w.writerow([
                prompt,
                resp.text,
                f"{resp.latency_ms:.3f}",
                resp.tokens_in,
                resp.tokens_out,
            ])


def estimate_cost(tokens_in: int, tokens_out: int) -> dict:
    """
    Tiny offline cost model (per 1K tokens). Adjust freely for your provider.
    """
    in_rate = 0.0005
    out_rate = 0.0015
    cost = (tokens_in / 1000.0) * in_rate + (tokens_out / 1000.0) * out_rate
    return {
        "usd": round(cost, 6),
        "rates_per_1k": {"input": in_rate, "output": out_rate},
    }
