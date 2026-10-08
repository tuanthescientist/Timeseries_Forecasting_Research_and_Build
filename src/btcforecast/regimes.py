"""Regime boundaries are fitted once on the declared training segment."""
from __future__ import annotations

import math
import statistics
from dataclasses import dataclass


def trailing_volatility(history: list[float], lookback: int = 30) -> float:
    if (not isinstance(lookback, int) or lookback < 1 or len(history) < lookback + 1
            or any(not math.isfinite(p) or p <= 0 for p in history)):
        raise ValueError("Insufficient positive history")
    values = history[-(lookback + 1):]
    returns = [math.log(b / a) for a, b in zip(values, values[1:], strict=False)]
    return statistics.pstdev(returns)


def quantile(values: list[float], probability: float) -> float:
    values = sorted(values)
    if (not values or not 0 <= probability <= 1
            or any(not math.isfinite(value) for value in values)):
        raise ValueError("Invalid quantile input")
    position = (len(values) - 1) * probability
    lower, upper = math.floor(position), math.ceil(position)
    return values[lower] + (position - lower) * (values[upper] - values[lower])


@dataclass(frozen=True)
class RegimeThresholds:
    low: float
    high: float
    fitted_through: int

    @classmethod
    def fit(cls, prices: list[float], train_end: int, lookback: int = 30):
        if not lookback < train_end < len(prices):
            raise ValueError("Training segment is too short or out of bounds")
        # Slicing happens before any volatility computation: later values cannot enter fit.
        train = prices[:train_end + 1]
        vols = [trailing_volatility(train[:i + 1], lookback)
                for i in range(lookback, len(train))]
        return cls(quantile(vols, 1 / 3), quantile(vols, 2 / 3), train_end)

    def classify(self, volatility: float) -> str:
        if not math.isfinite(volatility) or volatility < 0:
            raise ValueError("Invalid volatility")
        return "low" if volatility <= self.low else "medium" if volatility <= self.high else "high"
