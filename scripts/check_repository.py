"""Offline structural checks for the active BTC project and preserved archive."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import unquote

from btcforecast.data import ROOT, verify_snapshot
from btcforecast.protocol import load_protocol

URL_PREFIX = (
    "https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/"
)
ALLOWED_MARKET_FILES = {"legacy/data/raw/vn30.csv", "legacy/data/raw/bid.csv"}


def main():
    errors = []
    load_protocol()
    manifest = json.loads((ROOT / "data/manifest.json").read_text())
    verify_snapshot("DEMO")
    if manifest["datasets"]["BTC"]["status"] == "locked":
        verify_snapshot("BTC")
    notebooks = list((ROOT / "notebooks").rglob("*.ipynb"))
    for path in notebooks:
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("nbformat") != 4 or not data.get("cells"):
            errors.append(f"Invalid notebook: {path}")
    archive = manifest["archived_notebook"]
    actual_hash = hashlib.sha256((ROOT / archive["path"]).read_bytes()).hexdigest()
    if actual_hash != archive["sha256"]:
        errors.append("Original BTC archive was modified")
    markdown = [ROOT / "README.md", ROOT / "CONTRIBUTING.md"]
    markdown += list((ROOT / "docs").rglob("*.md"))
    markdown += list((ROOT / "notebooks").rglob("*.md"))
    markdown += list((ROOT / "results/tables").rglob("*.md"))
    for path in markdown:
        text = path.read_text(encoding="utf-8")
        if re.search(r"[A-Za-z]:\\(?:Users|Data Science)\\|file://", text):
            errors.append(f"Local machine path: {path}")
        for link in re.findall(r"\]\(([^)\s]+)\)", text):
            if link.startswith(URL_PREFIX):
                marker = "/research/btc-interval-calibration/"
                if marker in link:
                    relative = unquote(link.split(marker, 1)[1].split("#", 1)[0])
                    if not (ROOT / relative).exists():
                        errors.append(f"Missing GitHub target: {relative}")
            elif not link.startswith(("https://", "http://", "mailto:", "#")):
                if not (path.parent / unquote(link.split("#", 1)[0])).exists():
                    errors.append(f"Broken relative link: {path}: {link}")
    tracked = subprocess.run(["git", "ls-files"], cwd=ROOT, check=True,
                             capture_output=True, text=True).stdout.splitlines()
    for name in tracked:
        parts = Path(name).parts
        if (any(part in {".venv", "venv", "lightning_logs", "__pycache__"} for part in parts)
                or name.startswith("results/local/") or "/results/local/" in name):
            errors.append(f"Tracked local artifact: {name}")
        if name.startswith("data/raw/") and name != "data/raw/.gitkeep":
            errors.append(f"Raw BTC data must remain local: {name}")
        if name.startswith("legacy/data/raw/") and name not in ALLOWED_MARKET_FILES | {
                "legacy/data/raw/.gitkeep"}:
            errors.append(f"Unlisted historical snapshot: {name}")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Offline checks passed: {len(notebooks)} active/archive notebooks; BTC status "
          f"{manifest['datasets']['BTC']['status']}; no model fitting or downloads.")


if __name__ == "__main__":
    main()
