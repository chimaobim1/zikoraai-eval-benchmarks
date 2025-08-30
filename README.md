# Measuring What Matters: A Benchmark Playbook for Multi-Agent AI
[![CI](https://github.com/chimaobim1/zikoraai-eval-benchmarks/actions/workflows/ci.yml/badge.svg)](https://github.com/chimaobim1/zikoraai-eval-benchmarks/actions)
![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)


**By Chima Obi, AI Data Scientist at ZikoraAI**

This repo is a minimal, reproducible benchmark harness for multi-agent AI themes:
- Latency
- Accuracy
- Hallucination risk (source-grounding)
- Fairness across African languages (Yoruba, Igbo, Hausa, Swahili)
- Cost awareness (token estimate)

It runs fully offline using a deterministic stub model so CI is green without API keys.

## Quickstart
```bash
# Python 3.11+
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Run all benchmarks (writes reports/)
python -m zikoraai_eval.bench

# Or:
python scripts/run_bench.py

# Run tests
pytest -q
