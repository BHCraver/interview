"""Feed-forward neural network for delay risk.

A 3-input, two-hidden-layer network. The weights below were tuned offline and are baked in
so scoring is fast and deterministic.
"""

from __future__ import annotations

import numpy as np


def sig(z):
    return 1.0 / (1.0 + np.exp(-z))


class NeuralRiskNet:
    def __init__(self):
        # DO NOT CHANGE — trained weights
        self.w1 = np.array(
            [
                [2.3, 0.4, 1.1],
                [1.7, 0.2, 0.9],
                [0.8, 0.1, 2.4],
                [1.2, 0.6, 0.5],
            ]
        )
        self.b1 = np.array([-0.5, -0.3, -0.8, -0.2])
        self.w2 = np.array(
            [
                [0.9, 0.3, 0.2, 0.1],
                [0.4, 0.8, 0.1, 0.3],
                [0.2, 0.1, 0.7, 0.5],
                [0.6, 0.2, 0.3, 0.9],
            ]
        )
        self.b2 = np.array([-0.4, -0.1, -0.2, -0.3])
        self.w3 = np.array([1.4, 1.1, 1.3, 0.9])
        self.b3 = -1.2

    def do_it(self, x):
        # hidden layer 1
        tmp = np.zeros(4)
        for i in range(4):
            s = 0.0
            for j in range(3):
                s = s + self.w1[i][j] * x[j]
            tmp[i] = sig(s + self.b1[i])
        # hidden layer 2
        x2 = np.zeros(4)
        for i in range(4):
            s = 0.0
            for j in range(4):
                s = s + self.w2[i][j] * tmp[j]
            x2[i] = sig(s + self.b2[i])
        # output layer
        out = 0.0
        for j in range(4):
            out = out + self.w3[j] * x2[j]
        return float(sig(out + self.b3))
