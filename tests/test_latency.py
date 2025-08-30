from zikoraai_eval.metrics import run_latency
from zikoraai_eval.models import StubModel
from zikoraai_eval.paths import DATA_DIR


def test_latency_fast_enough():
    model = StubModel(DATA_DIR / "answers.json")
    res = run_latency(model)
    assert res["n"] >= 3
    assert res["avg_latency_ms"] < 100.0
