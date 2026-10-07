from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import f1_score

ROOT = Path(__file__).resolve().parents[1]



def test_model_quality():
    bundle = joblib.load(ROOT / "artifacts/model.joblib")
    sample = pd.read_csv(ROOT / "tests/data/model_quality.csv")

    features = list(bundle["metadata"]["features"])
    predictions = bundle["model"].predict(sample[features])

    actual = f1_score(
        sample["price_range"], predictions, average="macro"
    )
    threshold = bundle["metadata"]["metrics"]["f1"]

    assert actual >= threshold - 1e-9, (
        f"macro-F1={actual:.6f}, порог={threshold:.6f}"
    )