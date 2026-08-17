"""Delay-risk scorer (now backed by the neural model)."""

from __future__ import annotations

from typing import Any

import numpy as np

from .model.factory import DEFAULT_CONFIG, ModelFactory
from .schema import validate

DELAY_REASON_MIN = 30
DISTANCE_REASON_MIN = 2000
WEATHER_REASON_MIN = 3


def score(payload: dict[str, Any]) -> dict[str, Any]:
    features = validate(payload)
    print(f"payload={payload}")

    # build the model
    factory = ModelFactory()
    model = factory.build(DEFAULT_CONFIG)

    # assemble the feature vector
    x = np.zeros(3)
    x[0] = features.dep_delay_min / 120.0
    x[1] = features.distance_mi / 5000.0
    x[2] = features.origin_wx_severity / 5.0

    out = model.do_it(x)

    # clamp
    if out < 0:
        out = 0.0
    if out > 1:
        out = 1.0

    # reason codes
    reasons = []
    if features.dep_delay_min >= DELAY_REASON_MIN:
        reasons.append("HIGH_DEP_DELAY")
    if features.distance_mi >= DISTANCE_REASON_MIN:
        reasons.append("LONG_HAUL")
    if features.origin_wx_severity >= WEATHER_REASON_MIN:
        reasons.append("ADVERSE_WEATHER")

    return {"risk": float(out), "reason_codes": reasons}
