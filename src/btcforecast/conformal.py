"""Sequential intervals with timestamped, horizon-specific realised residuals.

This corrects the order-statistic convention identified in the historical supplementary
helper. Time-series coverage is measured empirically; exchangeability is not assumed.
"""
from __future__ import annotations

import math
from dataclasses import dataclass


def conformal_quantile(scores: list[float], level: float) -> float:
    if not scores or any(not math.isfinite(s) or s < 0 for s in scores):
        raise ValueError("Scores must be finite, non-negative and non-empty")
    if level <= 0:
        return 0.0
    if level >= 1:
        return math.inf
    rank = math.ceil((len(scores) + 1) * level)
    # If the required finite-sample rank exceeds n, the honest interval is unbounded.
    return math.inf if rank > len(scores) else sorted(scores)[rank - 1]


@dataclass(frozen=True)
class Residual:
    origin: int
    horizon: int
    score: float
    issued_q: float | None = None

    @property
    def realised_at(self) -> int:
        return self.origin + self.horizon


class SequentialCalibrator:
    """Ingest only outcomes observed by the current origin; reject premature feedback."""

    def __init__(self, horizon: int, alpha: float, method: str = "rolling",
                 window: int = 500, gamma: float = 0.005):
        if horizon < 1 or not 0 < alpha < 1 or window < 1 or gamma <= 0:
            raise ValueError("Invalid calibration settings")
        if method not in {"static", "rolling", "aci"}:
            raise ValueError("Unknown calibration method")
        self.horizon, self.alpha, self.method = horizon, alpha, method
        self.window, self.gamma = window, gamma
        self.alpha_t = alpha
        self.pool: list[Residual] = []
        self.seen: set[int] = set()
        self.last_time = -1

    def observe(self, residual: Residual, now: int, *, warm: bool = False) -> None:
        if now < self.last_time:
            raise ValueError("Time must not move backwards")
        if residual.horizon != self.horizon:
            raise ValueError("Cannot pool horizons")
        if residual.realised_at > now:
            raise ValueError("Outcome is not observable yet")
        if residual.origin in self.seen:
            raise ValueError("Duplicate feedback")
        if not math.isfinite(residual.score) or residual.score < 0:
            raise ValueError("Invalid residual score")
        if self.method == "aci" and not warm:
            if residual.issued_q is None or math.isnan(residual.issued_q) or residual.issued_q < 0:
                raise ValueError("ACI feedback requires the issued threshold")
        if self.method != "static" or warm:
            self.pool.append(residual)
            self.pool.sort(key=lambda item: item.realised_at)
        if self.method == "aci" and not warm:
            miss = float(residual.score > residual.issued_q)
            self.alpha_t += self.gamma * (self.alpha - miss)
        self.seen.add(residual.origin)
        self.last_time = now

    def threshold(self, now: int) -> float:
        if now < self.last_time:
            raise ValueError("Time must not move backwards")
        if any(item.realised_at > now for item in self.pool):
            raise ValueError("Calibration contains unavailable outcomes")
        self.last_time = now
        source = self.pool if self.method == "static" else self.pool[-self.window:]
        level = 1 - (self.alpha_t if self.method == "aci" else self.alpha)
        return conformal_quantile([item.score for item in source], level)
