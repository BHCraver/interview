"""Baseline delay-risk scorer.

A transparent, hand-tuned linear model. Weights come from the ops team's historical
correlation analysis (see README). Deterministic by construction.
"""

from __future__ import annotations

from typing import Any

from .schema import FlightFeatures, validate

# Per-feature contribution to the raw risk score. Tuned so a "typical" on-time flight
# lands near 0 and a badly-delayed, long-haul, bad-weather flight saturates near 1.
DEP_DELAY_WEIGHT = 1 / 120  # per minute already delayed at departure
DISTANCE_WEIGHT = 0.2 / 5000  # per mile
WEATHER_WEIGHT = 0.08  # per severity point (0..5)

# Thresholds for reason codes.
DELAY_REASON_MIN = 30  # minutes
DISTANCE_REASON_MIN = 2000  # miles
WEATHER_REASON_MIN = 3  # severity


def _clamp01(x: float) -> float:
    """Clamp a value into the [0, 1] interval."""
    return max(0.0, min(1.0, x))


def _reason_codes(features: FlightFeatures) -> list[str]:
    reasons: list[str] = []
    if features.dep_delay_min >= DELAY_REASON_MIN:
        reasons.append("HIGH_DEP_DELAY")
    if features.distance_mi >= DISTANCE_REASON_MIN:
        reasons.append("LONG_HAUL")
    if features.origin_wx_severity >= WEATHER_REASON_MIN:
        reasons.append("ADVERSE_WEATHER")
    return reasons


def score(payload: dict[str, Any]) -> dict[str, Any]:
    """Return the delay risk for a flight payload."""
    features = validate(payload)

    raw = (
        features.dep_delay_min * DEP_DELAY_WEIGHT
        + features.distance_mi * DISTANCE_WEIGHT
        + features.origin_wx_severity * WEATHER_WEIGHT
    )

    return {
        "risk": _clamp01(raw),
        "reason_codes": _reason_codes(features),
    }
