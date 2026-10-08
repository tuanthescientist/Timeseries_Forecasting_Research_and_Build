"""Endpoint baselines using only the supplied history through the origin."""
from __future__ import annotations

import math


def persistence(history: list[float], horizon: int) -> float:
    if not history or horizon < 1:
        raise ValueError("Non-empty history and positive horizon required")
    return float(history[-1])


def drift(history: list[float], horizon: int, window: int = 252) -> float:
    """Geometric drift from trailing Low-to-Low log changes, not return-MAPE."""
    if len(history) < 2 or horizon < 1 or window < 1 or min(history) <= 0:
        raise ValueError("Invalid history, horizon or window")
    values = history[-(window + 1):]
    mean = math.log(values[-1] / values[0]) / (len(values) - 1)
    return history[-1] * math.exp(horizon * mean)
