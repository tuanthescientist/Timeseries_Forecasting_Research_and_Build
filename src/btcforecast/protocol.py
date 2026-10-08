"""Canonical configuration hashing and honest prospective-stage gates."""
from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def fingerprint(config: dict) -> str:
    return hashlib.sha256(json.dumps(config, sort_keys=True, separators=(",", ":"),
                                     allow_nan=False).encode()).hexdigest()


def load_protocol(root: Path = ROOT) -> tuple[dict, str]:
    config = json.loads((root / "configs/protocol.json").read_text(encoding="utf-8"))
    lock = json.loads((root / "configs/protocol-lock.json").read_text(encoding="utf-8"))
    digest = fingerprint(config)
    if digest != lock["sha256"]:
        raise ValueError("Protocol differs from its recorded design lock")
    if config["horizons"] != [1, 5, 20, 30] or config["target"] != "low":
        raise ValueError("Unexpected task")
    for name, expected in lock["artifacts"].items():
        if hashlib.sha256((root / name).read_bytes()).hexdigest() != expected:
            raise ValueError(f"Design artifact changed: {name}")
    return config, digest


def _git(root: Path, *arguments: str) -> bytes:
    return subprocess.run(["git", *arguments], cwd=root, check=True, capture_output=True).stdout


def require_prospective(root: Path = ROOT, *, today: date | None = None) -> dict:
    """Require genuine pre-start freezes and complete outcomes; perform no forecasting."""
    config, digest = load_protocol(root)
    tag = config["design_tag"]
    lock = json.loads((root / "configs/protocol-lock.json").read_text())
    for name in ["configs/protocol.json", "configs/protocol-lock.json", *lock["artifacts"]]:
        if _git(root, "show", tag + ":" + name) != (root / name).read_bytes():
            raise ValueError(f"Artifact differs from foundation tag: {name}")
    completion = root / "results/tables/retrospective_completion.json"
    if not completion.exists():
        raise ValueError("Stages A–D are not completed and frozen")
    if lock["scope"] != "full_study":
        raise ValueError("Foundation-only design is not a complete prospective preregistration")
    record = json.loads(completion.read_text(encoding="utf-8"))
    if record.get("protocol_sha256") != digest or record.get("stages") != ["A", "B", "C", "D"]:
        raise ValueError("Invalid completion record")
    freeze = record.get("freeze_commit")
    artifacts = record.get("artifacts")
    if not freeze or not isinstance(artifacts, dict) or not artifacts:
        raise ValueError("Completion requires a freeze commit and hashed artifacts")
    _git(root, "cat-file", "-e", freeze + "^{commit}")
    frozen_at = datetime.fromisoformat(
        _git(root, "show", "-s", "--format=%cI", freeze).decode().strip()
    ).astimezone(timezone.utc).date()
    tag_at = datetime.fromisoformat(
        _git(root, "show", "-s", "--format=%cI", tag + "^{commit}").decode().strip()
    ).astimezone(timezone.utc).date()
    start = date.fromisoformat(config["prospective"]["start"])
    if frozen_at >= start or tag_at >= start:
        raise ValueError("Freeze occurred after future-window start; publish an amendment")
    for name, expected in artifacts.items():
        path = (root / name).resolve()
        if (not path.is_relative_to((root / "results/tables").resolve())
                or not name.startswith("results/tables/")):
            raise ValueError("Completion artifacts must stay within results/tables")
        historical = _git(root, "show", freeze + ":" + name)
        if hashlib.sha256(historical).hexdigest() != expected or path.read_bytes() != historical:
            raise ValueError(f"Completion artifact mismatch: {name}")
    from .data import verify_snapshot

    verify_snapshot("BTC", root / "data/manifest.json")
    manifest_bytes = _git(root, "show", freeze + ":data/manifest.json")
    frozen_btc = json.loads(manifest_bytes)["datasets"]["BTC"]
    current_btc = json.loads((root / "data/manifest.json").read_text())["datasets"]["BTC"]
    if frozen_btc != current_btc or frozen_btc.get("status") != "locked":
        raise ValueError("BTC snapshot was not locked in the pre-start freeze")
    if (today or datetime.now(timezone.utc).date()) <= date.fromisoformat(
            config["prospective"]["end"]):
        raise ValueError("Prospective window is not complete")
    return config
