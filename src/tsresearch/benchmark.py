"""Direct forecasts with labels available at each rolling forecast origin.

Horizons count observations, not calendar days. No network access is required.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
from datetime import date
from pathlib import Path

import numpy as np

WARMUP = 21


def load_series(path: Path) -> tuple[list[str], np.ndarray]:
    """Read an explicitly selected ds,y CSV; reject ambiguous input."""
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not {"ds", "y"}.issubset(reader.fieldnames or []):
            raise ValueError("CSV must contain ds and y columns")
        rows = list(reader)
    dates = [row["ds"] for row in rows]
    try:
        parsed = [date.fromisoformat(item) for item in dates]
        values = np.asarray([float(row["y"]) for row in rows], dtype=float)
    except (ValueError, TypeError) as exc:
        raise ValueError("Use ISO dates (YYYY-MM-DD) and numeric y values") from exc
    if not rows or any(b <= a for a, b in zip(parsed, parsed[1:])):
        raise ValueError("Dates must be unique and strictly increasing")
    if not np.all(np.isfinite(values)) or np.any(values <= 0):
        raise ValueError("Prices must be finite and strictly positive")
    return dates, values


def features(values: np.ndarray, index: int) -> np.ndarray:
    """Only observations up to and including index are visible."""
    if index < WARMUP:
        raise ValueError("Insufficient feature history")
    log_history = np.log(values[index - WARMUP:index + 1])
    returns = np.diff(log_history)
    return np.asarray(
        [log_history[-1] - log_history[-1 - lag] for lag in (1, 2, 3, 7, 14, 21)]
        + [returns[-window:].std() for window in (7, 21)]
    )


def training_indices(origin: int, horizon: int) -> np.ndarray:
    """A training label at t+h is usable only when t+h <= origin."""
    if horizon < 1:
        raise ValueError("Horizon must be positive")
    return np.arange(WARMUP, origin - horizon + 1)


def predict(values: np.ndarray, origin: int, horizon: int,
            alpha: float = 10.0) -> dict[str, float]:
    if horizon < 1 or not np.isfinite(alpha) or alpha <= 0:
        raise ValueError("Horizon and ridge alpha must be positive")
    if origin >= len(values) or origin < WARMUP + horizon + 1:
        raise ValueError("Invalid origin or insufficient training history")
    # Deliberately restrict every model to the available prefix.
    history = np.asarray(values[:origin + 1], dtype=float)
    if not np.all(np.isfinite(history)) or np.any(history <= 0):
        raise ValueError("History must contain finite positive prices")
    indices = training_indices(origin, horizon)
    x = np.vstack([features(history, int(i)) for i in indices])
    target = np.log(history[indices + horizon] / history[indices])
    mean = x.mean(axis=0)
    std = x.std(axis=0)
    std[std < 1e-12] = 1.0
    x = (x - mean) / std
    target_mean = target.mean()
    coef = np.linalg.solve(x.T @ x + alpha * np.eye(x.shape[1]),
                           x.T @ (target - target_mean))
    future_return = float(((features(history, origin) - mean) / std) @ coef + target_mean)
    last = float(history[-1])
    forecasts = {
        "naive": last,
        "drift": last + horizon * float(history[-1] - history[0]) / origin,
        "ridge_returns": last * float(np.exp(future_return)),
    }
    if not all(np.isfinite(value) for value in forecasts.values()):
        raise ValueError("Nonfinite prediction; inspect data scale and model stability")
    return forecasts


def evaluate(dates: list[str], values: np.ndarray, horizons: tuple[int, ...] = (1, 7, 30),
             folds: int = 12, step: int = 7, min_train: int = 90,
             alpha: float = 10.0) -> tuple[list[dict], list[dict]]:
    if len(dates) != len(values):
        raise ValueError("Dates and prices must have matching lengths")
    if not horizons or any(h < 1 for h in horizons) or len(set(horizons)) != len(horizons):
        raise ValueError("Horizons must be distinct positive integers")
    if folds < 1 or step < 1 or min_train < 2:
        raise ValueError("Invalid fold, step, or minimum training count")
    last_origin = len(values) - 1 - max(horizons)
    origins = list(range(last_origin - (folds - 1) * step, last_origin + 1, step))
    if len(training_indices(origins[0], max(horizons))) < min_train:
        raise ValueError("Insufficient data: reduce folds/horizon or supply more observations")
    predictions = []
    for origin in origins:
        for horizon in horizons:
            for model, yhat in predict(values, origin, horizon, alpha).items():
                predictions.append({
                    "origin": dates[origin], "target_date": dates[origin + horizon],
                    "horizon": horizon, "model": model,
                    "actual": float(values[origin + horizon]), "prediction": yhat,
                    "train_samples": len(training_indices(origin, horizon)),
                })
    metrics = []
    for horizon in horizons:
        for model in ("naive", "drift", "ridge_returns"):
            group = [row for row in predictions if row["horizon"] == horizon and row["model"] == model]
            actual = np.asarray([row["actual"] for row in group])
            predicted = np.asarray([row["prediction"] for row in group])
            error = predicted - actual
            metrics.append({"horizon": horizon, "model": model, "n_origins": len(group),
                            "mae": float(np.abs(error).mean()),
                            "rmse": float(np.sqrt(np.mean(error ** 2))),
                            "mape_percent": float(np.mean(np.abs(error) / actual) * 100)})
    return predictions, metrics


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("results/local"))
    parser.add_argument("--horizons", type=int, nargs="+", default=[1, 7, 30])
    parser.add_argument("--folds", type=int, default=12)
    parser.add_argument("--step", type=int, default=7)
    parser.add_argument("--min-train", type=int, default=90)
    parser.add_argument("--alpha", type=float, default=10.0)
    args = parser.parse_args()
    dates, values = load_series(args.csv)
    predictions, metrics = evaluate(dates, values, tuple(args.horizons), args.folds,
                                    args.step, args.min_train, args.alpha)
    args.output.mkdir(parents=True, exist_ok=True)
    write_csv(args.output / "predictions.csv", predictions)
    write_csv(args.output / "metrics.csv", metrics)
    metadata = {
        "input_file": args.csv.name,
        "input_sha256": hashlib.sha256(args.csv.read_bytes()).hexdigest(),
        "benchmark_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "rows": len(values), "start": dates[0], "end": dates[-1],
        "horizons_observations": args.horizons, "folds": args.folds,
        "step_observations": args.step, "min_train": args.min_train,
        "ridge_alpha": args.alpha, "python": platform.python_version(), "numpy": np.__version__,
        "protocol": "expanding-window, direct horizons, refit per origin; labels <= origin",
        "uncertainty": "Overlapping origins are dependent; no confidence intervals computed.",
    }
    (args.output / "run.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"Saved {len(predictions)} predictions and {len(metrics)} metric rows to {args.output}")


if __name__ == "__main__":
    main()
