# zikoraai-eval-benchmarks

[![CI](https://github.com/chimaobim1/zikoraai-eval-benchmarks/actions/workflows/ci.yml/badge.svg)](https://github.com/chimaobim1/zikoraai-eval-benchmarks/actions)
![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)

📌 By Chima Obi, AI Data Scientist at ZikoraAI  

Artificial Intelligence systems rarely fail because they cannot generate outputs. They fail because we do not measure them properly.

With multi-agent platforms, the risks compound: multiple models pass tasks around, interact in unpredictable ways, and small errors quickly grow into systemic failures. If you are not measuring latency, accuracy, fairness, and hallucination risk, you are building on weak foundations.

At ZikoraAI, we built a lightweight benchmark playbook that anyone can adopt. It’s not about flashy dashboards. It’s about simple scripts, clear datasets, and reproducible results. That’s what makes trust in multi-agent AI possible.


What We Measure

Latency – average response time in ms

Accuracy – unit tests on known inputs

Hallucination risk – tracing claims to retrieval sources

Fairness in African languages – Yoruba, Igbo, Hausa, Swahili

Cost awareness – tokens in/out per task

See the Evaluation Card
 for full scope, metrics, and limitations.
Sample output: EXAMPLE_summary.md

# example drop-in model
from dataclasses import dataclass
from zikoraai_eval.models import BaseModel, ModelResponse
import time

@dataclass
class MyAPIModel(BaseModel):
    api_key: str

    def generate(self, prompt: str) -> ModelResponse:
        t0 = time.perf_counter()
        # call your provider here...
        text = "demo answer"
        latency_ms = (time.perf_counter() - t0)*1000
        return ModelResponse(
            text=text,
            tokens_in=len(prompt)//4,
            tokens_out=len(text)//4,
            latency_ms=latency_ms,
        )


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
