"""Locate the repository, load the configured datasets and store notebook artefacts.

Real market files live in ``data/raw/`` (ignored by Git). When none is present, or when
``TSR_FORCE_DEMO=1``, notebooks fall back to the synthetic demo series so that every
notebook still runs end to end; demo results are written under ``results/local/``.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from .data import Dataset, load_prices
from .protocol import Protocol, load_protocol


def repo_root(start: str | Path | None = None) -> Path:
    here = Path(start or Path.cwd()).resolve()
    for folder in (here, *here.parents):
        if (folder / "configs" / "protocol.json").exists():
            return folder
    raise FileNotFoundError("Run from inside the repository (configs/protocol.json not found)")


@dataclass
class Study:
    """A dataset together with its fixed protocol and output locations."""

    name: str
    dataset: Dataset
    protocol: Protocol
    demo: bool
    root: Path

    @property
    def cache_dir(self) -> Path:
        return self.root / "results" / "local" / "cache"

    def output_dir(self) -> Path:
        base = self.root / "results"
        folder = base / "local" / "demo" if self.demo else base / self.name.lower()
        folder.mkdir(parents=True, exist_ok=True)
        return folder

    def save_table(self, table: pd.DataFrame, name: str) -> Path:
        path = self.output_dir() / f"{name}.csv"
        table.to_csv(path, index=False, float_format="%.6g", lineterminator="\n")
        return path

    def save_figure(self, figure, name: str) -> Path:
        path = self.output_dir() / f"{name}.png"
        figure.savefig(path, dpi=130, bbox_inches="tight")
        return path

    def save_json(self, payload: dict, name: str) -> Path:
        path = self.output_dir() / f"{name}.json"
        path.write_text(json.dumps(payload, indent=2, default=str) + "\n", encoding="utf-8",
                        newline="\n")
        return path


def load_studies(root: str | Path | None = None, force_demo: bool | None = None) -> list[Study]:
    """Studies for every configured real dataset that is present, else the demo series."""
    root = repo_root(root)
    config = json.loads((root / "configs" / "datasets.json").read_text(encoding="utf-8"))
    protocols = root / "configs" / "protocol.json"
    if force_demo is None:
        force_demo = os.environ.get("TSR_FORCE_DEMO", "") not in ("", "0")
    studies = []
    if not force_demo:
        for name, entry in config.items():
            if name == "DEMO":
                continue
            path = root / entry["file"]
            if path.exists():
                studies.append(Study(name, load_prices(path, name),
                                     load_protocol(protocols, name), False, root))
    if not studies:
        demo = root / config["DEMO"]["file"]
        studies.append(Study("DEMO", load_prices(demo, "DEMO"),
                             load_protocol(protocols, "DEMO"), True, root))
    return studies
