"""Loads the trained XGBoost model once and turns form input into a tip prediction."""
from functools import lru_cache
from pathlib import Path

import joblib
import pandas as pd

MODEL_PATH = Path(__file__).resolve().parent / "ml_models" / "xgb_model.joblib"

# Column order used during training in 01_ml.ipynb (X = df.drop("tip", axis=1)).
FEATURES = ["total_bill", "sex", "smoker", "day", "time", "size"]

# The notebook used sklearn's LabelEncoder, which numbers classes alphabetically.
# Reproduced here explicitly because the saved label_encoder.pickle was re-fitted
# on the last column ("time") only, so it cannot decode sex/smoker/day.
ENCODING = {
    "sex": {"Female": 0, "Male": 1},
    "smoker": {"No": 0, "Yes": 1},
    "day": {"Fri": 0, "Sat": 1, "Sun": 2, "Thur": 3},
    "time": {"Dinner": 0, "Lunch": 1},
}

# Hold-out test metrics from the notebook (XGBoost, 80/20 split, random_state=42).
MODEL_MAE = 0.6722
MODEL_R2 = 0.4088


@lru_cache(maxsize=1)
def get_model():
    return joblib.load(MODEL_PATH)


def predict_tip(data: dict) -> dict:
    row = {
        "total_bill": float(data["total_bill"]),
        "sex": ENCODING["sex"][data["sex"]],
        "smoker": ENCODING["smoker"][data["smoker"]],
        "day": ENCODING["day"][data["day"]],
        "time": ENCODING["time"][data["time"]],
        "size": int(data["size"]),
    }
    frame = pd.DataFrame([row], columns=FEATURES)
    tip = max(float(get_model().predict(frame)[0]), 0.0)
    bill = row["total_bill"]
    return {
        "tip": round(tip, 2),
        "tip_percent": round(tip / bill * 100, 1),
        "per_person": round(tip / row["size"], 2),
        "total": round(bill + tip, 2),
        "low": round(max(tip - MODEL_MAE, 0), 2),
        "high": round(tip + MODEL_MAE, 2),
    }
