markdown
# Evaluation Card: zikoraai-eval-benchmarks

**Scope:** Offline, deterministic harness for demonstrating evaluation practice on multi-agent themes:
latency, accuracy, fairness (African langs), hallucination risk, cost.

**Model:** `StubModel` (no external calls). Deterministic lookup via `data/answers.json`.

**Datasets (toy):**
- `data/prompts.csv`: 3 QA items (accuracy/latency)
- `data/fairness.csv`: Yoruba, Igbo, Hausa, Swahili “good morning”
- `data/claims.csv`: 2 grounding checks with source markers

**Metrics:**
- Accuracy: exact(ish) string match on toy set
- Latency: avg + p95 in ms
- Fairness: per-language accuracy + gap (max–min)
- Hallucination risk: 0 (grounded) or 1 (not grounded)
- Cost: simple token-based estimate

**Reproducibility:**
- `pytest -q` matches CI
- All outputs written to `reports/` (JSON/CSV/MD)
- No API keys required

**Limitations:**
- Toy data; meant for pedagogy & CI reproducibility
- Swap in real models by implementing `BaseModel.generate`
