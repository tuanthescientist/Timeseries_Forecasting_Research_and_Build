"""Rolling-origin baseline evidence; scales and predictors see origin history only."""
from __future__ import annotations

import math
import statistics

from .baselines import drift, persistence
from .regimes import RegimeThresholds, trailing_volatility


def eligible_labels(origins: list[int], horizon: int, now: int) -> list[int]:
    if horizon < 1:
        raise ValueError("Positive horizon required")
    return [origin for origin in origins if origin + horizon <= now]


def mase_denominator(training: list[float]) -> float:
    if len(training) < 2:
        raise ValueError("Training segment too short")
    scale = statistics.mean(abs(b - a) for a, b in zip(training, training[1:], strict=False))
    if scale <= 0:
        raise ValueError("MASE undefined for constant training data")
    return scale


def backtest(rows: list[dict], horizons: list[int], start: int, end: int,
             train_end: int, lookback: int = 30, drift_window: int = 252) -> list[dict]:
    prices = [row["low"] for row in rows]
    if not horizons or any(h < 1 for h in horizons):
        raise ValueError("Invalid horizons")
    if not lookback < train_end < start <= end < len(rows):
        raise ValueError("Invalid stage boundaries")
    thresholds = RegimeThresholds.fit(prices, train_end, lookback)
    denominator = mase_denominator(prices[:train_end + 1])
    records = []
    for origin in range(start, end + 1):
        history = prices[:origin + 1]
        vol = trailing_volatility(history, lookback)
        for horizon in horizons:
            if origin + horizon > end:
                continue
            for name, predict in (("persistence", persistence), ("drift", drift)):
                pred = predict(history, horizon) if name == "persistence" else predict(
                    history, horizon, drift_window)
                records.append({"model": name, "origin": origin,
                                "origin_date": rows[origin]["date"],
                                "horizon": horizon, "target_date": rows[origin + horizon]["date"],
                                "pred": pred, "actual": prices[origin + horizon],
                                "origin_low": prices[origin], "volatility": vol,
                                "regime": thresholds.classify(vol), "mase_scale": denominator})
    return records


def summarise(records: list[dict]) -> list[dict]:
    groups = {}
    for row in records:
        groups.setdefault((row["model"], int(row["horizon"])), []).append(row)
    result = []
    for (model, horizon), group in sorted(groups.items()):
        errors = [abs(float(r["actual"]) - float(r["pred"])) for r in group]
        result.append({"model": model, "horizon": horizon, "n": len(group),
                       "mae": statistics.mean(errors),
                       "rmse": math.sqrt(statistics.mean(e * e for e in errors)),
                       "mase": statistics.mean(e / float(r["mase_scale"])
                                               for e, r in zip(errors, group, strict=True))})
    return result
