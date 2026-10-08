"""Causal features and multi-horizon targets.

Row ``i`` of the feature table uses observations ``0..i`` only (the forecast origin is
after row ``i`` is known). Targets are log returns ``log(y[i+h] / y[i])`` and are NaN
where the future row does not exist. Nothing here looks forward except the targets.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from .data import OHLC, invalid_ohlc

WARMUP = 60
EWMA_LAMBDA = 0.94


def ewma_volatility(log_returns: pd.Series, decay: float = EWMA_LAMBDA) -> pd.Series:
    """RiskMetrics-style volatility of one-step log returns, known at each row."""
    variance = (log_returns ** 2).ewm(alpha=1 - decay, adjust=False, min_periods=20).mean()
    return np.sqrt(variance)


def build_features(frame: pd.DataFrame) -> pd.DataFrame:
    """Return a feature table aligned with ``frame``; missing inputs become flagged zeros."""
    y = frame["y"].astype(float)
    ret = np.log(y).diff()
    bad = invalid_ohlc(frame)
    op, hi, lo = (frame[c].astype(float).mask(bad) for c in OHLC)
    volume = frame["volume"].astype(float)
    volume = volume.where(np.isfinite(volume) & (volume > 0))

    f = pd.DataFrame(index=frame.index)
    for lag in range(10):
        f[f"ret_lag{lag}"] = ret.shift(lag)
    for window in (5, 10, 20, 60):
        f[f"mom_{window}"] = np.log(y / y.shift(window))
        f[f"vol_{window}"] = ret.rolling(window, min_periods=window).std()
    f["vol_ewma"] = ewma_volatility(ret)
    f["dist_ma20"] = np.log(y / y.rolling(20, min_periods=20).mean())
    f["drift_252"] = ret.rolling(252, min_periods=60).mean()
    gain = ret.clip(lower=0).rolling(14, min_periods=14).mean()
    loss = (-ret.clip(upper=0)).rolling(14, min_periods=14).mean()
    f["rsi14"] = 100 * gain / (gain + loss).replace(0, np.nan)
    f["gap"] = np.log(op / y.shift(1))
    f["body"] = np.log(y / op)
    f["range"] = np.log(hi / lo)
    f["close_location"] = (y - lo) / (hi - lo).replace(0, np.nan)
    f["log_volume_rel20"] = np.log(volume / volume.rolling(20, min_periods=10).median())
    f["calendar_gap"] = frame["calendar_gap"].astype(float)
    f["ohlc_missing"] = (bad | op.isna()).astype(float)
    f["volume_missing"] = volume.isna().astype(float)
    f = f.replace([np.inf, -np.inf], np.nan).ffill().fillna(0.0)
    return f.astype(float)


def targets(prices: np.ndarray, horizons: tuple[int, ...]) -> np.ndarray:
    """Matrix of h-step log returns, shape (n, len(horizons)); NaN past the last row."""
    logp = np.log(np.asarray(prices, dtype=float))
    out = np.full((len(logp), len(horizons)), np.nan)
    for j, h in enumerate(horizons):
        out[: len(logp) - h, j] = logp[h:] - logp[: len(logp) - h]
    return out
