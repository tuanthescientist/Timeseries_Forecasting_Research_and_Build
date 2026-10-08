"""Offline structural checks, including raw-data policy at every directory depth."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import PurePosixPath
from urllib.parse import unquote

from btcforecast.data import ROOT, verify_snapshot
from btcforecast.protocol import load_protocol

URL_PREFIX = "https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/"


def forbidden_raw_path(name: str) -> bool:
    parts = PurePosixPath(name.replace("\\", "/")).parts
    contains_raw = any(parts[index:index + 2] == ("data", "raw")
                       for index in range(len(parts) - 1))
    return contains_raw and parts[-1] != ".gitkeep"


def check_market_manifest(manifest: dict) -> None:
    record = manifest["datasets"]["BTC"]
    if record["status"] != "locked":
        return
    if not re.fullmatch(r"[a-f0-9]{64}", record.get("sha256") or ""):
        raise ValueError("Locked BTC manifest needs a SHA-256")
    if not record.get("retrieved_at_utc") or not record.get("rows", 0) > 0:
        raise ValueError("Locked BTC manifest needs retrieval time and row count")
    # A fresh CI checkout deliberately has no vendor CSV. Verify local bytes when present.
    if (ROOT / record["path"]).exists():
        verify_snapshot("BTC")
    results_manifest = ROOT / "results/tables/stage_a_run.json"
    if results_manifest.exists():
        run = json.loads(results_manifest.read_text(encoding="utf-8"))
        if run["snapshot_sha256"] != record["sha256"] or run["synthetic"]:
            raise ValueError("Published Stage A metadata does not match the BTC snapshot")


def main():
    errors = []
    load_protocol()
    manifest = json.loads((ROOT / "data/manifest.json").read_text())
    verify_snapshot("DEMO")
    check_market_manifest(manifest)
    notebooks = list((ROOT / "notebooks").rglob("*.ipynb"))
    for path in notebooks:
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("nbformat") != 4 or not data.get("cells"):
            errors.append(f"Invalid notebook: {path}")
    archive = manifest["archived_notebook"]
    if hashlib.sha256((ROOT / archive["path"]).read_bytes()).hexdigest() != archive["sha256"]:
        errors.append("Original BTC archive was modified")
    markdown = [ROOT / "README.md", ROOT / "CONTRIBUTING.md"]
    for folder in ("docs", "notebooks", "results/tables", "legacy/docs"):
        markdown += list((ROOT / folder).rglob("*.md"))
    markdown += [ROOT / "legacy/README.md"]
    for path in markdown:
        text = path.read_text(encoding="utf-8")
        if re.search(r"[A-Za-z]:\\(?:Users|Data Science)\\|file://", text):
            errors.append(f"Local machine path: {path}")
        for link in re.findall(r"\]\(([^)\s]+)\)", text):
            if link.startswith(URL_PREFIX):
                for marker in ("/blob/main/", "/tree/main/"):
                    if marker in link:
                        relative = unquote(link.split(marker, 1)[1].split("#", 1)[0])
                        if not (ROOT / relative).exists():
                            errors.append(f"Missing GitHub main target: {relative}")
            elif not link.startswith(("https://", "http://", "mailto:", "#")):
                if not (path.parent / unquote(link.split("#", 1)[0])).exists():
                    errors.append(f"Broken relative link: {path}: {link}")
    tracked = subprocess.run(["git", "ls-files"], cwd=ROOT, check=True,
                             capture_output=True, text=True).stdout.splitlines()
    for name in tracked:
        parts = PurePosixPath(name).parts
        if (any(part in {".venv", "venv", "lightning_logs", "__pycache__"} for part in parts)
                or name.startswith("results/local/") or "/results/local/" in name):
            errors.append(f"Tracked local artifact: {name}")
        if forbidden_raw_path(name):
            errors.append(f"Raw vendor data must remain local, including legacy: {name}")
    if errors:
        raise SystemExit("\n".join(errors))
    status = manifest["datasets"]["BTC"]["status"]
    print(f"Offline checks passed: {len(notebooks)} notebooks; BTC {status}")


if __name__ == "__main__":
    main()
