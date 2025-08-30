from zikoraai_eval.metrics import run_hallucination
from zikoraai_eval.models import StubModel
from zikoraai_eval.paths import DATA_DIR


def test_hallucination_grounded():
    model = StubModel(DATA_DIR / "answers.json")
    res = run_hallucination(model)
    assert res["n"] >= 2
    assert res["avg_risk"] == 0.0
