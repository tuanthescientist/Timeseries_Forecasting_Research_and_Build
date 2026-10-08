"""Acquire a NEW snapshot or restore exact locked bytes; no downloads occur in CI."""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.metadata
import json
from datetime import date, datetime, timezone

from btcforecast.data import COLUMNS, ROOT, read_snapshot


def main(*, restore: bool = False):
    import yfinance as yf

    config = json.loads((ROOT / "configs/btc.json").read_text())
    settings = config["download"]
    if datetime.now(timezone.utc).date() < date.fromisoformat(settings["end_exclusive"]):
        raise SystemExit("Requested last UTC day has not closed yet")
    target = ROOT / config["local_path"]
    manifest_path = ROOT / "data/manifest.json"
    manifest = json.loads(manifest_path.read_text())
    record = manifest["datasets"]["BTC"]
    if target.exists():
        raise SystemExit("Refusing to overwrite an existing snapshot")
    if restore and record["status"] != "locked":
        raise SystemExit("--restore requires a published locked manifest")
    if not restore and record["status"] == "locked":
        raise SystemExit("Snapshot already locked; use --restore to recover matching local bytes")
    download_args = {key: value for key, value in settings.items() if key != "end_exclusive"}
    download_args["end"] = settings["end_exclusive"]
    frame = yf.download(config["instrument"], **download_args, progress=False)
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
        digest = hashlib.sha256(temporary.read_bytes()).hexdigest()
        if restore:
            if digest != record["sha256"]:
                raise ValueError("Provider bytes changed; restore refused. "
                                 "Document a new snapshot.")
            temporary.replace(target)
            receipt = ROOT / "results/local/btc-restore.json"
            receipt.parent.mkdir(parents=True, exist_ok=True)
            receipt.write_text(json.dumps({"restored_at_utc": stamp, "sha256": digest}, indent=2),
                               encoding="utf-8", newline="\n")
        else:
            record.update(status="locked", sha256=digest, rows=len(rows),
                          first_date=rows[0]["date"], last_date=rows[-1]["date"],
                          retrieved_at_utc=stamp,
                          yfinance_version=importlib.metadata.version("yfinance"))
            temporary.replace(target)
            manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8",
                                     newline="\n")
    finally:
        if temporary.exists():
            temporary.unlink()
    print("Restored matching local BTC bytes." if restore else "Locked NEW BTC snapshot.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--restore", action="store_true")
    main(restore=parser.parse_args().restore)
