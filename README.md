# zikoraai-eval-benchmarks

[![CI](https://github.com/chimaobim1/zikoraai-eval-benchmarks/actions/workflows/ci.yml/badge.svg)](https://github.com/chimaobim1/zikoraai-eval-benchmarks/actions)
![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)

📌 By Chima Obi, AI Data Scientist at ZikoraAI  

Artificial Intelligence systems rarely fail because they cannot generate outputs. They fail because we do not measure them properly.

With multi-agent platforms, the risks compound: multiple models pass tasks around, interact in unpredictable ways, and small errors quickly grow into systemic failures. If you are not measuring latency, accuracy, fairness, and hallucination risk, you are building on weak foundations.

At ZikoraAI, we built a lightweight benchmark playbook that anyone can adopt. It’s not about flashy dashboards. It’s about simple scripts, clear datasets, and reproducible results. That’s what makes trust in multi-agent AI possible.

---

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
