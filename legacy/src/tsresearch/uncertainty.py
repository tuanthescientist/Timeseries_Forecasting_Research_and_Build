"""Assemble and summarise prediction intervals for one forecasting model."""

from __future__ import annotations

import numpy as np
import pandas as pd

from .conformal import conformal_intervals, gaussian_intervals
from .metrics import coverage, interval_score

METHODS = ("gaussian_vol", "static_abs", "rolling_abs", "static_norm", "rolling_norm",
           "aci_norm")
LABELS = {
    "gaussian_vol": "Gaussian, EWMA volatility (no calibration)",
    "static_abs": "Split conformal, absolute residuals (static)",
    "rolling_abs": "Split conformal, absolute residuals (rolling)",
    "static_norm": "Split conformal, volatility-normalised (static)",
    "rolling_norm": "Split conformal, volatility-normalised (rolling)",
    "aci_norm": "Adaptive conformal (ACI), volatility-normalised",
}


def _scale(g: pd.DataFrame, horizon: int, normalised: bool) -> np.ndarray:
    if not normalised:
        return np.ones(len(g))
    scale = g["vol_ewma"].to_numpy(float) * np.sqrt(horizon)
    if not (scale > 0).all():
        raise ValueError("Volatility scale must be positive")
    return scale


def build_intervals(validation: pd.DataFrame, test: pd.DataFrame, alphas=(0.2, 0.05),
                    window: int = 500, gamma: float = 0.005) -> pd.DataFrame:
    """Intervals on the test origins for every method, horizon and miscoverage level.

    ``validation`` and ``test`` are backtest outputs of the *same* model. Validation
    residuals provide the warm start; test outcomes enter calibration only after they
    are realised (``origin + horizon <= current origin``).
    """
    if validation["model"].nunique() != 1 or test["model"].nunique() != 1:
        raise ValueError("Pass predictions of a single model")
    frames = []
    for horizon in sorted(test["horizon"].unique()):
        v = validation[validation["horizon"] == horizon].sort_values("origin")
        t = test[test["horizon"] == horizon].sort_values("origin")
        for alpha in alphas:
            for method in METHODS:
                normalised = method.endswith("_norm") or method == "gaussian_vol"
                if method == "gaussian_vol":
                    lo, hi = gaussian_intervals(t["pred"], _scale(t, horizon, True), alpha)
                    used = np.full(len(t), alpha)
                else:
                    kind, _ = method.split("_")
                    residual = np.abs(v["actual"] - v["pred"]).to_numpy()
                    warm = residual / _scale(v, horizon, normalised)
                    lo, hi, used = conformal_intervals(
                        t["origin"].to_numpy(), t["pred"], t["actual"],
                        _scale(t, horizon, normalised), horizon, alpha, warm,
                        method=kind, window=window, gamma=gamma)
                frames.append(pd.DataFrame({
                    "method": method, "horizon": horizon, "alpha": alpha,
                    "origin": t["origin"].to_numpy(), "origin_date": t["origin_date"].to_numpy(),
                    "pred": t["pred"].to_numpy(), "actual": t["actual"].to_numpy(),
                    "vol_ewma": t["vol_ewma"].to_numpy(), "lower": lo, "upper": hi,
                    "alpha_used": used}))
    return pd.concat(frames, ignore_index=True)


def summarise_intervals(intervals: pd.DataFrame) -> pd.DataFrame:
    """Coverage, mean width and interval score per method, horizon and level."""
    rows = []
    for (method, horizon, alpha), g in intervals.groupby(["method", "horizon", "alpha"],
                                                         sort=False):
        rows.append({"method": method, "horizon": int(horizon), "nominal": 1 - alpha,
                     "coverage": coverage(g["lower"], g["upper"], g["actual"]),
                     "mean_width": float((g["upper"] - g["lower"]).mean()),
                     "interval_score": interval_score(g["lower"], g["upper"], g["actual"], alpha),
                     "n": len(g)})
    out = pd.DataFrame(rows)
    out["coverage_gap"] = out["coverage"] - out["nominal"]
    return out


def coverage_by_regime(intervals: pd.DataFrame, edges: tuple[float, float]) -> pd.DataFrame:
    """Coverage within low/medium/high trailing-volatility regimes.

    ``edges`` are volatility terciles taken from the *validation* segment, so regimes are
    defined without test information.
    """
    labels = np.where(intervals["vol_ewma"] <= edges[0], "low vol",
                      np.where(intervals["vol_ewma"] <= edges[1], "mid vol", "high vol"))
    frame = intervals.assign(regime=labels)
    frame["hit"] = (frame["actual"] >= frame["lower"]) & (frame["actual"] <= frame["upper"])
    out = frame.groupby(["method", "horizon", "alpha", "regime"], sort=False).agg(
        coverage=("hit", "mean"), n=("hit", "size")).reset_index()
    out["nominal"] = 1 - out["alpha"]
    return out
