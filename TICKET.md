# TICKET DR-142 — Improve the delay-risk model

The hand-tuned linear baseline in `src/delay_risk/predict.py` works, but the ops team wants a
**more accurate** delay-risk score before we expose it to the crew-scheduling app.

**Ask**
- Upgrade the scorer to something more accurate than the linear baseline.
- Keep the public contract stable: `score(payload) -> {"risk": float in [0,1], "reason_codes": [...]}`.
- Keep it deterministic.

**Definition of done**
- Same input/output contract (or a documented, tested change).
- Tests updated.
- Show the new model **beats the current baseline** on the labeled sample (`eval/backtest.py`).
