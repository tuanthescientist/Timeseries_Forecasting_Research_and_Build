"""Point, interval and comparison metrics for h-step return forecasts."""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats

from .data import Dataset
from .protocol import Protocol, segment_origins


def rmse(error) -> float:
    return float(np.sqrt(np.mean(np.square(error))))


def mae(error) -> float:
    return float(np.mean(np.abs(error)))


def mase_scale(dataset: Dataset, protocol: Protocol) -> dict[int, float]:
    """In-sample naive MAE per horizon, using only rows before the validation segment.

    For a return target the persistence forecast is zero, so the scale is the mean
    absolute h-step log return observed before the first validation origin.
    """
    first_validation = int(segment_origins(dataset.dates, protocol)["validation"][0])
    logp = np.log(dataset.prices[: first_validation + 1])
    return {h: float(np.mean(np.abs(logp[h:] - logp[:-h]))) for h in protocol.horizons}


def directional_accuracy(pred, actual) -> float:
    """Share of non-zero realised moves whose sign was forecast (50% is chance-like)."""
    pred, actual = np.asarray(pred), np.asarray(actual)
    moved = actual != 0
    if not moved.any() or not (pred != 0).any():
        return float("nan")
    return float(np.mean(np.sign(pred[moved]) == np.sign(actual[moved])))


def point_metrics(predictions: pd.DataFrame, scale: dict[int, float] | None = None) -> pd.DataFrame:
    """Per model and horizon: errors, ratios to persistence and price-level MAPE.

    ``rel_rmse``/``rel_mae`` divide by the persistence (zero-return) error on the same
    origins, so values below 1 beat persistence. ``mase`` uses the in-sample ``scale``.
    """
    rows = []
    for (model, horizon), g in predictions.groupby(["model", "horizon"], sort=False):
        error = g["pred"] - g["actual"]
        zero_rmse, zero_mae = rmse(g["actual"]), mae(g["actual"])
        row = {"model": model, "horizon": int(horizon), "n_origins": len(g),
               "rmse": rmse(error), "mae": mae(error),
               "rel_rmse": rmse(error) / zero_rmse, "rel_mae": mae(error) / zero_mae,
               "direction_acc": directional_accuracy(g["pred"], g["actual"]),
               "price_mape_pct": float(np.mean(np.abs(g["price_pred"] - g["price_target"])
                                               / g["price_target"]) * 100)}
        if scale is not None:
            row["mase"] = mae(error) / scale[int(horizon)]
        rows.append(row)
    return pd.DataFrame(rows)


def loss_differential(predictions: pd.DataFrame, model_a: str, model_b: str, horizon: int,
                      loss: str = "squared") -> pd.Series:
    """Per-origin ``loss(a) - loss(b)``; negative values favour ``model_a``."""
    g = predictions[predictions["horizon"] == horizon]
    a = g[g["model"] == model_a].set_index("origin")
    b = g[g["model"] == model_b].set_index("origin")
    if not a.index.equals(b.index):
        raise ValueError("Models must be evaluated on identical origins")
    if loss == "squared":
        la, lb = (a["pred"] - a["actual"]) ** 2, (b["pred"] - b["actual"]) ** 2
    elif loss == "absolute":
        la, lb = (a["pred"] - a["actual"]).abs(), (b["pred"] - b["actual"]).abs()
    else:
        raise ValueError("loss must be 'squared' or 'absolute'")
    return la - lb


def diebold_mariano(d, horizon: int) -> dict[str, float]:
    """Diebold-Mariano test on a loss differential with a Bartlett HAC variance.

    Overlapping h-step forecasts make errors serially dependent up to lag h-1; the
    long-run variance uses that many lags. The Harvey-Leybourne-Newbold small-sample
    correction and a Student-t reference distribution are applied.
    """
    d = np.asarray(d, dtype=float)
    n = len(d)
    if n < 10:
        raise ValueError("Need at least 10 origins")
    centred = d - d.mean()
    lags = max(horizon - 1, 0)
    long_run = float(np.mean(centred ** 2))
    for k in range(1, lags + 1):
        weight = 1 - k / (lags + 1)
        long_run += 2 * weight * float(np.mean(centred[k:] * centred[:-k]))
    long_run = max(long_run, 1e-300)
    stat = d.mean() / np.sqrt(long_run / n)
    correction = np.sqrt((n + 1 - 2 * horizon + horizon * (horizon - 1) / n) / n)
    stat *= correction
    p_value = 2 * stats.t.sf(abs(stat), df=n - 1)
    return {"mean_diff": float(d.mean()), "dm_stat": float(stat), "p_value": float(p_value)}


def holm_adjust(p_values) -> np.ndarray:
    """Holm-Bonferroni adjusted p-values for a family of simultaneous tests."""
    p = np.asarray(p_values, dtype=float)
    order = np.argsort(p)
    adjusted = np.empty_like(p)
    running = 0.0
    for rank, index in enumerate(order):
        running = max(running, (len(p) - rank) * p[index])
        adjusted[index] = min(1.0, running)
    return adjusted


def block_bootstrap_ci(d, block: int, n_boot: int = 2000, seed: int = 0,
                       level: float = 0.95) -> tuple[float, float]:
    """Circular block bootstrap interval for the mean of a dependent series."""
    d = np.asarray(d, dtype=float)
    n = len(d)
    rng = np.random.default_rng(seed)
    block = max(1, min(int(block), n))
    n_blocks = int(np.ceil(n / block))
    starts = rng.integers(0, n, size=(n_boot, n_blocks))
    index = (starts[:, :, None] + np.arange(block)[None, None, :]) % n
    means = d[index.reshape(n_boot, -1)[:, :n]].mean(axis=1)
    lo, hi = np.quantile(means, [(1 - level) / 2, 1 - (1 - level) / 2])
    return float(lo), float(hi)


def best_per_family(table: pd.DataFrame, specs: list[dict], names: dict[int, str] | None = None
                    ) -> pd.DataFrame:
    """Rank candidate specs by mean ``rel_rmse`` over horizons (validation use only).

    Returns one row per spec with its family and score, sorted so that the first row of
    each family is that family's choice. Persistence has score 1 by construction.
    """
    from .models import spec_name
    by_name = {spec_name(s): s for s in specs}
    score = table.groupby("model")["rel_rmse"].mean().rename("mean_rel_rmse").reset_index()
    score["family"] = score["model"].map(lambda m: by_name[m]["family"])
    return score.sort_values(["family", "mean_rel_rmse"]).reset_index(drop=True)


def coverage(lower, upper, actual) -> float:
    actual = np.asarray(actual)
    return float(np.mean((actual >= np.asarray(lower)) & (actual <= np.asarray(upper))))


def interval_score(lower, upper, actual, alpha: float) -> float:
    """Winkler/interval score: width plus penalties for misses (lower is better)."""
    lower, upper, actual = (np.asarray(v, dtype=float) for v in (lower, upper, actual))
    score = (upper - lower) + (2 / alpha) * (lower - actual) * (actual < lower) \
        + (2 / alpha) * (actual - upper) * (actual > upper)
    return float(np.mean(score))


def pinball_loss(actual, quantile_pred, tau: float) -> float:
    diff = np.asarray(actual, dtype=float) - np.asarray(quantile_pred, dtype=float)
    return float(np.mean(np.maximum(tau * diff, (tau - 1) * diff)))
