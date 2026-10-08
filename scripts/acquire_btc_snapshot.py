"""Explicit Yahoo acquisition. Creates a NEW snapshot, never the recovered original."""
from __future__ import annotations

import csv
import hashlib
import importlib.metadata
import json
from datetime import date, datetime, timezone

from btcforecast.data import COLUMNS, ROOT, read_snapshot


def main():
    import yfinance as yf

    config_path = ROOT / "configs/btc.json"
    config = json.loads(config_path.read_text())
    settings = config["download"]
    if datetime.now(timezone.utc).date() < date.fromisoformat(settings["end_exclusive"]):
        raise SystemExit("Requested last UTC day has not closed yet")
    target = ROOT / config["local_path"]
    manifest_path = ROOT / "data/manifest.json"
    manifest = json.loads(manifest_path.read_text())
    if target.exists() or manifest["datasets"]["BTC"]["status"] == "locked":
        raise SystemExit("Refusing to overwrite a snapshot; create a documented amendment")
    frame = yf.download(config["instrument"], **settings, progress=False)
    if frame.empty:
        raise SystemExit("Yahoo returned no data")
    if getattr(frame.columns, "nlevels", 1) > 1:
        frame.columns = frame.columns.get_level_values(0)
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_suffix(".pending.csv")
    try:
        with temporary.open("x", encoding="utf-8", newline="") as stream:
            writer = csv.writer(stream)
            writer.writerow(COLUMNS)
            for stamp, row in frame.iterrows():
                if stamp.tzinfo is not None:
                    stamp = stamp.tz_convert("UTC")
                writer.writerow([stamp.date().isoformat()] + [format(float(row[name]), ".17g")
                                for name in ("Open", "High", "Low", "Close", "Volume")])
        rows = read_snapshot(temporary)
        if rows[0]["date"] != settings["start"]:
            raise ValueError("First requested date is missing")
        expected_end = date.fromisoformat(settings["end_exclusive"]).toordinal() - 1
        if date.fromisoformat(rows[-1]["date"]).toordinal() != expected_end:
            raise ValueError("Last completed day is missing")
        stamp = datetime.now(timezone.utc).isoformat()
        record = manifest["datasets"]["BTC"]
        record.update(status="locked", sha256=hashlib.sha256(temporary.read_bytes()).hexdigest(),
                      rows=len(rows), first_date=rows[0]["date"], last_date=rows[-1]["date"],
                      retrieved_at_utc=stamp,
                      yfinance_version=importlib.metadata.version("yfinance"))
        # configs/btc.json is design-locked: acquisition evidence belongs only in the manifest.
        temporary.replace(target)
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    finally:
        if temporary.exists():
            temporary.unlink()
    print("Locked NEW BTC snapshot. Original notebook bytes were not recovered.")


if __name__ == "__main__":
    main()
