"""Prediction intervals for h-step returns with sequential (online) calibration.

All methods wrap point forecasts. For an origin ``o`` and horizon ``h`` the outcome is
known only at ``o + h``, so a calibration score may be used at origin ``k`` only if
``origin_j + h <= origin_k``. Scores from the validation segment are all realised before
the first test origin and serve as the warm start.

Methods
-------
``static``   split conformal: quantile of the warm-start scores, never updated;
``rolling``  split conformal on the most recent ``window`` realised scores;
``aci``      adaptive conformal inference (Gibbs & Candes, 2021): the miscoverage level
             is nudged by ``gamma * (alpha - miss)`` whenever an outcome is realised.
Scores are ``|actual - pred| / scale``; ``scale=1`` gives absolute-residual intervals and
``scale=vol_ewma*sqrt(h)`` gives volatility-normalised intervals.
"""

from __future__ import annotations

import numpy as np
from scipy import stats


def conformal_quantile(scores: np.ndarray, level: float) -> float:
    """Finite-sample-corrected empirical quantile of non-negative scores."""
    scores = np.asarray(scores, dtype=float)
    n = len(scores)
    if n == 0:
        raise ValueError("No calibration scores")
    if level >= 1.0:
        return float(scores.max())
    if level <= 0.0:
        return 0.0
    rank = min(1.0, np.ceil((n + 1) * level) / n)
    return float(np.quantile(scores, rank, method="higher"))


def conformal_intervals(origin, pred, actual, scale, horizon: int, alpha: float,
                        warm_scores, method: str = "rolling", window: int = 500,
                        gamma: float = 0.005):
    """Intervals for consecutive origins; returns ``(lower, upper, miscoverage_path)``.

    ``miscoverage_path`` is the nominal level actually used at each origin (it differs
    from ``alpha`` only for ``aci``).
    """
    if method not in {"static", "rolling", "aci"}:
        raise ValueError("method must be static, rolling or aci")
    origin = np.asarray(origin)
    pred, actual, scale = (np.asarray(v, dtype=float) for v in (pred, actual, scale))
    warm_scores = np.asarray(warm_scores, dtype=float)
    n = len(origin)
    lower, upper, used = np.empty(n), np.empty(n), np.empty(n)
    q_used = np.empty(n)
    pool = list(warm_scores)
    alpha_t = alpha
    pointer = 0
    for k in range(n):
        while pointer < k and origin[pointer] + horizon <= origin[k]:
            score = abs(actual[pointer] - pred[pointer]) / scale[pointer]
            pool.append(score)
            if method == "aci":
                miss = float(score > q_used[pointer])
                alpha_t += gamma * (alpha - miss)
            pointer += 1
        if method == "static":
            source, level = warm_scores, 1 - alpha
        elif method == "rolling":
            source, level = np.asarray(pool[-window:]), 1 - alpha
        else:
            source, level = np.asarray(pool[-window:]), 1 - alpha_t
        q_used[k] = conformal_quantile(source, level)
        used[k] = alpha_t if method == "aci" else alpha
        lower[k] = pred[k] - q_used[k] * scale[k]
        upper[k] = pred[k] + q_used[k] * scale[k]
    return lower, upper, used


def gaussian_intervals(pred, scale, alpha: float):
    """Normal intervals ``pred +/- z * scale`` (volatility-scaled Gaussian baseline)."""
    z = stats.norm.ppf(1 - alpha / 2)
    pred, scale = np.asarray(pred, dtype=float), np.asarray(scale, dtype=float)
    return pred - z * scale, pred + z * scale


def rolling_mean(values, window: int) -> np.ndarray:
    values = np.asarray(values, dtype=float)
    kernel = np.ones(window) / window
    return np.convolve(values, kernel, mode="valid")
