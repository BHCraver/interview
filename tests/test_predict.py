from __future__ import annotations

import pytest

from delay_risk import score

VALID = {"flight_id": "AS123", "dep_delay_min": 20, "distance_mi": 800, "origin_wx_severity": 1}


def test_returns_expected_keys():
    out = score(VALID)
    assert set(out.keys()) == {"risk", "reason_codes"}


def test_risk_is_in_unit_interval():
    out = score({"flight_id": "AS1", "dep_delay_min": 100000, "distance_mi": 999999, "origin_wx_severity": 5})
    assert 0.0 <= out["risk"] <= 1.0


def test_is_deterministic():
    assert score(VALID) == score(VALID)


def test_reason_codes_fire_on_thresholds():
    out = score({"flight_id": "AS9", "dep_delay_min": 45, "distance_mi": 2500, "origin_wx_severity": 4})
    assert out["reason_codes"] == ["HIGH_DEP_DELAY", "LONG_HAUL", "ADVERSE_WEATHER"]


def test_invalid_input_raises():
    with pytest.raises(ValueError, match="dep_delay_min"):
        score({"flight_id": "AS9", "dep_delay_min": -1, "distance_mi": 800})
