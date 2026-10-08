"""Offline CSV validation. Acquisition is explicit and never called by CI."""
from __future__ import annotations

import csv
import hashlib
import json
import math
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COLUMNS = ("date", "open", "high", "low", "close", "volume")


def read_snapshot(path: Path) -> list[dict]:
    """Require one ordered UTC calendar-day observation and consistent positive OHLC."""
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != list(COLUMNS):
            raise ValueError(f"Expected columns: {COLUMNS}")
        rows = list(reader)
    if not rows:
        raise ValueError("Empty snapshot")
    previous = None
    for row in rows:
        stamp = date.fromisoformat(row["date"])
        if previous is not None and stamp != previous + timedelta(days=1):
            raise ValueError(f"Duplicate, unordered or missing daily observation: {stamp}")
        values = {name: float(row[name]) for name in COLUMNS[1:]}
        if not all(math.isfinite(value) for value in values.values()):
            raise ValueError("Non-finite numeric observation")
        if min(values[name] for name in ("open", "high", "low", "close")) <= 0:
            raise ValueError("Prices must be positive")
        if values["volume"] < 0:
            raise ValueError("Volume must be non-negative")
        if not (values["low"] <= min(values["open"], values["close"])
                <= max(values["open"], values["close"]) <= values["high"]):
            raise ValueError(f"Inconsistent OHLC: {stamp}")
        row.update(values)
        previous = stamp
    return rows


def verify_snapshot(key: str, manifest_path: Path | None = None) -> list[dict]:
    manifest_path = manifest_path or ROOT / "data/manifest.json"
    record = json.loads(manifest_path.read_text(encoding="utf-8"))["datasets"][key]
    if record["status"] != "locked":
        raise ValueError(f"{key} snapshot is not locked; no saved original BTC bytes are available")
    path = ROOT / record["path"]
    if hashlib.sha256(path.read_bytes()).hexdigest() != record["sha256"]:
        raise ValueError("Snapshot hash mismatch")
    rows = read_snapshot(path)
    if len(rows) != record["rows"]:
        raise ValueError("Snapshot row count mismatch")
    if rows[0]["date"] != record["first_date"] or rows[-1]["date"] != record["last_date"]:
        raise ValueError("Snapshot date range mismatch")
    return rows
