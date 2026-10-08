"""Rolling-origin backtests with periodic refitting and enforced label availability."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict
from pathlib import Path

import numpy as np
import pandas as pd

from .data import Dataset
from .features import WARMUP, build_features, targets
from .models import make_model, spec_name
from .protocol import Protocol, segment_origins

_CODE_FILES = ("backtest.py", "features.py", "models.py", "protocol.py")


def _code_fingerprint() -> str:
    folder = Path(__file__).parent
    digest = hashlib.sha256()
    for name in _CODE_FILES:
        digest.update((folder / name).read_bytes())
    return digest.hexdigest()[:16]


def _cache_path(cache_dir: Path, dataset: Dataset, spec: dict, protocol: Protocol,
                segment: str) -> Path:
    key = json.dumps({"data": dataset.sha256, "spec": spec, "protocol": asdict(protocol),
                      "segment": segment, "code": _code_fingerprint()}, sort_keys=True)
    return cache_dir / f"{hashlib.sha256(key.encode()).hexdigest()[:20]}.csv"


def run_backtest(dataset: Dataset, spec: dict, protocol: Protocol, segment: str,
                 features: pd.DataFrame | None = None, cache_dir: str | Path | None = None,
                 ) -> pd.DataFrame:
    """Forecast every origin of ``segment`` and return one row per origin and horizon.

    The model is refitted every ``protocol.refit_every`` origins. At a refit origin ``o``
    it may use training rows ``t`` only if the *longest* label ``t + max(horizons)`` is
    already observed (``<= o``), so no label crosses the origin. Forecasts for the next
    origins reuse that fit with their own (causal) feature rows.
    """
    path = None
    if cache_dir is not None:
        path = _cache_path(Path(cache_dir), dataset, spec, protocol, segment)
        if path.exists():
            return pd.read_csv(path, parse_dates=["origin_date", "target_date"])

    frame = dataset.frame
    prices = dataset.prices
    dates = dataset.dates
    X_all = (features if features is not None else build_features(frame))
    columns = list(X_all.columns)
    X_values = X_all.to_numpy(float)
    horizons = protocol.horizons
    h_max = protocol.max_horizon
    Y_all = targets(prices, horizons)
    origins = segment_origins(dates, protocol)[segment]
    predictions = np.empty((len(origins), len(horizons)))

    for start in range(0, len(origins), protocol.refit_every):
        block = origins[start:start + protocol.refit_every]
        refit_origin = int(block[0])
        last_row = refit_origin - h_max
        first_row = WARMUP if protocol.train_window is None else max(
            WARMUP, last_row - protocol.train_window + 1)
        rows = np.arange(first_row, last_row + 1)
        if len(rows) == 0 or rows[-1] + h_max > refit_origin:
            raise AssertionError("Training labels must be observed at the refit origin")
        Y_train = Y_all[rows]
        if not np.isfinite(Y_train).all():
            raise AssertionError("Non-finite training label")
        model = make_model(spec, horizons, columns).fit(X_values[rows], Y_train)
        predictions[start:start + len(block)] = model.predict(X_values[block])

    name = spec_name(spec)
    records = []
    for j, h in enumerate(horizons):
        target_rows = origins + h
        records.append(pd.DataFrame({
            "model": name, "segment": segment, "horizon": h,
            "origin": origins, "origin_date": dates[origins], "target_date": dates[target_rows],
            "pred": predictions[:, j], "actual": Y_all[origins, j],
            "price_origin": prices[origins], "price_target": prices[target_rows],
            "vol_ewma": X_all["vol_ewma"].to_numpy(float)[origins],
        }))
    result = pd.concat(records, ignore_index=True)
    result["price_pred"] = result["price_origin"] * np.exp(result["pred"])
    result = result.sort_values(["horizon", "origin"]).reset_index(drop=True)
    if path is not None:
        path.parent.mkdir(parents=True, exist_ok=True)
        result.to_csv(path, index=False)
    return result


def run_specs(dataset: Dataset, specs: list[dict], protocol: Protocol, segment: str,
              cache_dir: str | Path | None = None, verbose: bool = False) -> pd.DataFrame:
    """Backtest several model specifications on identical origins."""
    features = build_features(dataset.frame)
    frames = []
    for spec in specs:
        if verbose:
            print(f"  {dataset.name} {segment}: {spec_name(spec)}", flush=True)
        frames.append(run_backtest(dataset, spec, protocol, segment, features, cache_dir))
    return pd.concat(frames, ignore_index=True)
