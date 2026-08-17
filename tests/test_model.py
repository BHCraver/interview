from __future__ import annotations

import numpy as np

from delay_risk.model.factory import DEFAULT_CONFIG, ModelFactory


def test_model_builds_and_scores():
    model = ModelFactory().build(DEFAULT_CONFIG)
    x = np.array([0.1, 0.2, 0.0])
    assert round(model.do_it(x), 6) == 0.844009
