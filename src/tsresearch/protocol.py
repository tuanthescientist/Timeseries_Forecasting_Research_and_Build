"""Chronological segments and rolling forecast origins.

An origin ``o`` means rows ``0..o`` are known and the forecast targets ``y[o+h]``.
Segments are defined by dates fixed in ``configs/protocol.json`` *before* any model is run:

* ``train``       rows before ``validation_start`` (model fitting only);
* ``validation``  origins from ``validation_start`` whose longest target ends before
                  ``test_start`` (hyper-parameter choice and conformal warm start);
* ``test``        origins from ``test_start`` (touched once, with frozen choices).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, replace
from pathlib import Path

import numpy as np
import pandas as pd

from .features import WARMUP


@dataclass(frozen=True)
class Protocol:
    validation_start: str
    test_start: str
    horizons: tuple[int, ...] = (1, 5, 20)
    refit_every: int = 20
    min_train: int = 750
    train_window: int | None = None

    @property
    def max_horizon(self) -> int:
        return max(self.horizons)

    def with_updates(self, **changes) -> Protocol:
        return replace(self, **changes)


def load_protocol(path: str | Path, name: str) -> Protocol:
    """Read one named protocol from the JSON manifest."""
    entry = json.loads(Path(path).read_text(encoding="utf-8"))[name]
    entry = dict(entry)
    entry["horizons"] = tuple(entry.get("horizons", (1, 5, 20)))
    return Protocol(**entry)


def _first_index_on_or_after(dates: pd.DatetimeIndex, day: str) -> int:
    index = int(dates.searchsorted(pd.Timestamp(day), side="left"))
    if index >= len(dates):
        raise ValueError(f"No observation on or after {day}")
    return index


def segment_origins(dates: pd.DatetimeIndex, protocol: Protocol) -> dict[str, np.ndarray]:
    """Eligible origins per segment; every origin has all horizons observable."""
    n = len(dates)
    h_max = protocol.max_horizon
    first = WARMUP + protocol.min_train
    val_start = max(_first_index_on_or_after(dates, protocol.validation_start), first)
    test_start = _first_index_on_or_after(dates, protocol.test_start)
    if test_start <= val_start + protocol.refit_every:
        raise ValueError("Validation segment is empty; adjust dates or min_train")
    validation = np.arange(val_start, test_start - h_max)
    test = np.arange(test_start, n - h_max)
    if len(test) < protocol.refit_every:
        raise ValueError("Test segment is too short for the chosen horizons")
    return {"validation": validation, "test": test}


def segment_table(dates: pd.DatetimeIndex, protocol: Protocol) -> pd.DataFrame:
    """Human-readable description of the segments (for notebooks and docs)."""
    origins = segment_origins(dates, protocol)
    first_train = WARMUP
    rows = [{"segment": "train (fit only)", "first_origin": dates[first_train],
             "last_origin": dates[origins["validation"][0] - 1],
             "origins": int(origins["validation"][0] - first_train)}]
    for name in ("validation", "test"):
        o = origins[name]
        rows.append({"segment": name, "first_origin": dates[o[0]], "last_origin": dates[o[-1]],
                     "origins": int(len(o))})
    return pd.DataFrame(rows)
