"""Input validation for the delay-risk scorer."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

_REQUIRED = ("flight_id", "dep_delay_min", "distance_mi")


@dataclass(frozen=True)
class FlightFeatures:
    flight_id: str
    dep_delay_min: int
    distance_mi: int
    origin_wx_severity: int = 0


def validate(payload: dict[str, Any]) -> FlightFeatures:
    """Validate a raw payload and return typed features.

    Raises ValueError with a clear message on invalid input.
    """
    missing = [key for key in _REQUIRED if key not in payload]
    if missing:
        raise ValueError(f"missing required field(s): {', '.join(missing)}")

    flight_id = payload["flight_id"]
    if not isinstance(flight_id, str) or not flight_id.strip():
        raise ValueError("flight_id must be a non-empty string")

    dep_delay_min = payload["dep_delay_min"]
    if not isinstance(dep_delay_min, int) or dep_delay_min < 0:
        raise ValueError("dep_delay_min must be an int >= 0")

    distance_mi = payload["distance_mi"]
    if not isinstance(distance_mi, int) or distance_mi <= 0:
        raise ValueError("distance_mi must be an int > 0")

    origin_wx_severity = payload.get("origin_wx_severity", 0)
    if not isinstance(origin_wx_severity, int) or not 0 <= origin_wx_severity <= 5:
        raise ValueError("origin_wx_severity must be an int in 0..5")

    return FlightFeatures(
        flight_id=flight_id,
        dep_delay_min=dep_delay_min,
        distance_mi=distance_mi,
        origin_wx_severity=origin_wx_severity,
    )
