"""Load daily price files and report data-quality problems without repairing them.

Two layouts are accepted:

* ``ds,y`` with optional ``open,high,low,volume`` columns and ISO dates;
* the common export layout ``Date,Price,Open,High,Low,Vol.,Change %`` with
  ``month/day/year`` dates, thousands separators and ``K/M/B`` volume suffixes.

Prices are never imputed. A row is one observation (a trading session or a bar);
returns are changes between consecutive rows, so missing sessions are visible in the
``calendar_gap`` column instead of being hidden.
"""

from __future__ import annotations

import hashlib
import io
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

OHLC = ("open", "high", "low")
_SUFFIX = {"B": 1e9, "M": 1e6, "K": 1e3}


@dataclass
class Dataset:
    """A validated price table plus the provenance needed to cite it."""

    name: str
    frame: pd.DataFrame
    sha256: str
    source: str
    reported_change: pd.Series | None = None

    def __len__(self) -> int:
        return len(self.frame)

    @property
    def dates(self) -> pd.DatetimeIndex:
        return pd.DatetimeIndex(self.frame["ds"])

    @property
    def prices(self) -> np.ndarray:
        return self.frame["y"].to_numpy(float)


def _to_number(series: pd.Series) -> pd.Series:
    text = series.astype(str).str.replace(",", "", regex=False).str.replace('"', "", regex=False)
    return pd.to_numeric(text.str.strip(), errors="coerce")


def _parse_volume(series: pd.Series) -> pd.Series:
    text = series.astype(str).str.upper().str.replace(r"[^0-9.BMK]", "", regex=True)
    suffix = text.str.extract(r"([BMK])$", expand=False).map(_SUFFIX).fillna(1.0)
    number = pd.to_numeric(text.str.replace(r"[BMK]$", "", regex=True), errors="coerce")
    return number * suffix


def _read_frame(raw: bytes) -> tuple[pd.DataFrame, pd.Series | None]:
    table = pd.read_csv(io.BytesIO(raw), encoding="utf-8-sig")
    columns = {c.strip().lower(): c for c in table.columns}
    reported = None
    if {"ds", "y"}.issubset(columns):
        frame = pd.DataFrame({"ds": pd.to_datetime(table[columns["ds"]], format="%Y-%m-%d",
                                                   errors="coerce"),
                              "y": _to_number(table[columns["y"]])})
        for name in (*OHLC, "volume"):
            frame[name] = _to_number(table[columns[name]]) if name in columns else np.nan
    elif {"date", "price"}.issubset(columns):
        frame = pd.DataFrame({"ds": pd.to_datetime(table[columns["date"]], format="%m/%d/%Y",
                                                   errors="coerce"),
                              "y": _to_number(table[columns["price"]])})
        for name in OHLC:
            frame[name] = _to_number(table[columns[name]]) if name in columns else np.nan
        vol_key = next((k for k in columns if k.startswith("vol")), None)
        frame["volume"] = _parse_volume(table[columns[vol_key]]) if vol_key else np.nan
        if "change %" in columns:
            reported = _to_number(table[columns["change %"]].astype(str).str.replace("%", ""))
    else:
        raise ValueError("CSV needs ds,y columns or Date,Price columns")
    return frame, reported


def load_prices(path: str | Path, name: str | None = None) -> Dataset:
    """Read a price CSV, sort it chronologically and refuse ambiguous input."""
    path = Path(path)
    raw = path.read_bytes()
    frame, reported = _read_frame(raw)
    if frame["ds"].isna().any() or frame["y"].isna().any():
        raise ValueError("Unparseable dates or prices; fix the source, nothing is imputed")
    if (frame["y"] <= 0).any() or not np.isfinite(frame["y"]).all():
        raise ValueError("Prices must be finite and strictly positive")
    if frame["ds"].duplicated().any():
        raise ValueError("Duplicate dates; check the source before running")
    order = np.argsort(frame["ds"].to_numpy())
    frame = frame.iloc[order].reset_index(drop=True)
    if reported is not None:
        reported = reported.iloc[order].reset_index(drop=True)
    frame["calendar_gap"] = frame["ds"].diff().dt.days.astype(float)
    return Dataset(name or path.stem, frame, hashlib.sha256(raw).hexdigest(), path.name,
                   reported)


def invalid_ohlc(frame: pd.DataFrame) -> pd.Series:
    """Rows whose open/high/low are missing or inconsistent with each other or the close."""
    o, h, low, c = (frame[k] for k in ("open", "high", "low", "y"))
    missing = frame[list(OHLC)].isna().any(axis=1)
    broken = ((h < low) | (o < low) | (o > h) | (c < low) | (c > h)
              | (frame[list(OHLC)] <= 0).any(axis=1))
    return missing | broken


def quality_report(dataset: Dataset, extreme_move: float = 0.10) -> dict:
    """Facts a reader needs before trusting a series; nothing here modifies the data."""
    frame = dataset.frame
    returns = np.log(frame["y"]).diff()
    has_ohlc = frame[list(OHLC)].notna().all(axis=1)
    bad = invalid_ohlc(frame) & has_ohlc
    report = {
        "name": dataset.name,
        "source_file": dataset.source,
        "sha256": dataset.sha256,
        "rows": len(frame),
        "first_date": str(frame["ds"].iloc[0].date()),
        "last_date": str(frame["ds"].iloc[-1].date()),
        "rows_with_ohlc": int(has_ohlc.sum()),
        "ohlc_inconsistent_rows": int(bad.sum()),
        "rows_with_volume": int(frame["volume"].notna().sum()),
        "weekend_dated_rows": int((frame["ds"].dt.dayofweek >= 5).sum()),
        "gaps_over_5_calendar_days": int((frame["calendar_gap"] > 5).sum()),
        "largest_gap_days": float(np.nanmax(frame["calendar_gap"])) if len(frame) > 1 else 0.0,
        "abs_log_return_over_threshold": int((returns.abs() > extreme_move).sum()),
        "extreme_move_threshold": extreme_move,
    }
    if dataset.reported_change is not None:
        calculated = 100 * frame["y"].pct_change()
        report["reported_change_mismatch_rows"] = int(
            ((dataset.reported_change - calculated).abs() > 0.1).sum())
    return report
