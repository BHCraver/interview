# delay-risk

A tiny service that scores a flight's **risk of arriving late** from a few pieces of
flight metadata. Returns a risk score in `[0, 1]` plus human-readable reason codes.

This is intentionally small and transparent. The current model is a **hand-tuned linear
baseline** — the weights were set by the ops team from historical correlations. It is the
number the rest of the team is trying to beat.

## Layout

```
src/delay_risk/
  schema.py      # input validation -> FlightFeatures
  predict.py     # the baseline scorer (score())
eval/
  backtest.py    # accuracy of the current scorer on the labeled sample
data/
  flights_sample.csv   # small labeled sample (fake, for local dev + backtest)
tests/
  test_predict.py
```

## Run

```bash
python -m pytest -q          # tests
python eval/backtest.py      # prints baseline accuracy on the sample
```

## Contract

Input (dict):
- `flight_id: str` (non-empty)
- `dep_delay_min: int` (>= 0)  — minutes the flight has already been delayed at departure
- `distance_mi: int` (> 0)
- `origin_wx_severity: int` (0..5, optional, default 0) — 0 clear ... 5 severe

Output (dict):
- `risk: float` in `[0, 1]`
- `reason_codes: list[str]`

Invalid input raises `ValueError` with a clear message. Same input always returns the same
output (deterministic).
