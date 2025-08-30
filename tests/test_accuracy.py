from zikoraai_eval.metrics import run_accuracy
from zikoraai_eval.models import StubModel
from zikoraai_eval.paths import DATA_DIR


def test_accuracy():
    model = StubModel(DATA_DIR / "answers.json")
    res = run_accuracy(model)
    assert res["n"] >= 3
    assert res["accuracy"] == 1.0
