# Measuring What Matters: A Benchmark Playbook for Multi-Agent AI
[![CI](https://github.com/chimaobim1/zikoraai-eval-benchmarks/actions/workflows/ci.yml/badge.svg)](https://github.com/chimaobim1/zikoraai-eval-benchmarks/actions)
![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)
Sample output: [EXAMPLE_summary.md](./reports/EXAMPLE_summary.md)

**By Chima Obi, AI Data Scientist at ZikoraAI**

This repo is a minimal, reproducible benchmark harness for multi-agent AI themes:
- Latency
- Accuracy
- Hallucination risk (source-grounding)
- Fairness across African languages (Yoruba, Igbo, Hausa, Swahili)
- Cost awareness (token estimate)

It runs fully offline using a deterministic stub model so CI is green without API keys.

## ✅ Reproduce in 60 seconds

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -e .            # installs zikoraai_eval for imports

# run everything
python -m zikoraai_eval.bench

# run tests (same as CI)
pytest -q

