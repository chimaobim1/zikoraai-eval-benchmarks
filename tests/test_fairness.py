from zikoraai_eval.metrics import run_fairness
from zikoraai_eval.models import StubModel
from zikoraai_eval.paths import DATA_DIR


def test_fairness_all_languages_pass():
    model = StubModel(DATA_DIR / "answers.json")
    res = run_fairness(model)
    per_lang = res["per_language_accuracy"]
    assert {"Yoruba", "Igbo", "Hausa", "Swahili"} <= set(per_lang.keys())
    assert all(v == 1.0 for v in per_lang.values())
    assert res["fairness_gap"] == 0.0
