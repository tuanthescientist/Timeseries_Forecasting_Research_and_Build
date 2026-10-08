"""Adapter for audited attention predictions, without silent training in CI."""
from __future__ import annotations

import csv
import math
from pathlib import Path


def load_attention_predictions(path: Path, observations: list[dict],
                               *, protocol_sha256: str) -> list[dict]:
    """Accept endpoint predictions only when metadata and observable cutoffs are explicit.

    This does not reproduce/retrain the original attention network. It checks a future
    export so its comparisons cannot silently reuse in-sample or recursive notebook plots.
    """
    required = {"origin", "horizon", "pred", "information_end", "trained_label_end",
                "selected_through", "protocol_sha256", "strategy"}
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        if not required.issubset(reader.fieldnames or []):
            raise ValueError("Incomplete prediction provenance")
        rows = list(reader)
    seen = set()
    for row in rows:
        origin, horizon = int(row["origin"]), int(row["horizon"])
        if horizon not in {1, 5, 20, 30} or not 0 <= origin < len(observations) - horizon:
            raise ValueError("Invalid origin or horizon")
        if row["strategy"] not in {"rolling_one_step", "direct", "recursive"}:
            raise ValueError("Unknown strategy")
        if row["strategy"] == "rolling_one_step" and horizon != 1:
            raise ValueError("One-step predictions cannot be relabelled as multi-step")
        if max(int(row[name]) for name in ("information_end", "trained_label_end",
                                          "selected_through")) > origin:
            raise ValueError("Prediction uses future information")
        if row["protocol_sha256"] != protocol_sha256:
            raise ValueError("Prediction protocol mismatch")
        key = (origin, horizon, row["strategy"])
        if key in seen:
            raise ValueError("Duplicate forecast")
        seen.add(key)
        if not math.isfinite(float(row["pred"])):
            raise ValueError("Non-finite forecast")
        row.update(origin=origin, horizon=horizon, pred=float(row["pred"]),
                   actual=observations[origin + horizon]["low"])
    return rows
