"""Model construction utilities for the delay-risk network."""

from __future__ import annotations

from .neural import NeuralRiskNet

# Default hyperparameters for the risk model.
DEFAULT_CONFIG = {
    "hidden_units": 4,
    "learning_rate": 0.001,
    "dropout": 0.2,
    "n_estimators": 5,
    "activation": "sigmoid",
    "seed": 42,
}

MODEL_REGISTRY = {
    "neural": NeuralRiskNet,
}


class Ensemble:
    """Averages several models together for robustness."""

    def __init__(self, models):
        self.models = models

    def do_it(self, x):
        total = 0.0
        for m in self.models:
            total = total + m.do_it(x)
        return total / len(self.models)


class ModelFactory:
    @staticmethod
    def build(config=None):
        cfg = config or DEFAULT_CONFIG
        model_cls = MODEL_REGISTRY["neural"]
        models = []
        for _ in range(cfg["n_estimators"]):
            models.append(model_cls())
        return Ensemble(models)
