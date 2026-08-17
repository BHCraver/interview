"""Offline backtest: how accurate is the current scorer on the labeled sample?

Run: python eval/backtest.py
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

# Make src/ importable when run as a script.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from delay_risk import score  # noqa: E402

DATA = Path(__file__).resolve().parents[1] / "data" / "flights_sample.csv"
DECISION_THRESHOLD = 0.5


def load_rows() -> list[dict]:
    with DATA.open(newline="") as fh:
        return list(csv.DictReader(fh))


def backtest() -> float:
    rows = load_rows()
    correct = 0
    for row in rows:
        payload = {
            "flight_id": row["flight_id"],
            "dep_delay_min": int(row["dep_delay_min"]),
            "distance_mi": int(row["distance_mi"]),
            "origin_wx_severity": int(row["origin_wx_severity"]),
        }
        predicted = 1 if score(payload)["risk"] >= DECISION_THRESHOLD else 0
        correct += int(predicted == int(row["delayed"]))
    return correct / len(rows)


if __name__ == "__main__":
    accuracy = backtest()
    print(f"current scorer accuracy on {DATA.name}: {accuracy:.3f}")
