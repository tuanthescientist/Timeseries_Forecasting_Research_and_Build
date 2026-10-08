"""Small offline experiment drivers; demo output is explicitly synthetic."""
from __future__ import annotations

import csv
import hashlib
import json
import math
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from .conformal import Residual, SequentialCalibrator
from .data import ROOT, verify_snapshot
from .evaluation import backtest, summarise
from .protocol import load_protocol


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        raise ValueError("No result rows")
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def begin_run(stage: str, dataset: str, root: Path = ROOT) -> tuple[Path, list[dict], dict]:
    config, digest = load_protocol(root)
    rows = verify_snapshot(dataset, root / "data/manifest.json")
    commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, check=True,
                            capture_output=True, text=True).stdout.strip()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    folder = root / "results/runs" / f"{stamp}-{commit[:8]}-{stage}"
    folder.mkdir(parents=True)
    metadata = {"stage": stage, "dataset": dataset, "synthetic": dataset == "DEMO",
                "protocol_sha256": digest, "commit": commit,
                "created_at_utc": datetime.now(timezone.utc).isoformat(),
                "snapshot_sha256": hashlib.sha256(
                    (root / ("data/demo/btc_daily.csv" if dataset == "DEMO"
                             else "data/raw/btc_usd_daily.csv")).read_bytes()).hexdigest(),
                "status": "running"}
    (folder / "run.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    return folder, rows, config


def split_indices(rows: list[dict], config: dict, demo: bool) -> tuple[int, int, int, int]:
    if demo:
        return 199, 250, 399, len(rows) - 1
    dates = [row["date"] for row in rows]
    train_end = dates.index(config["splits"]["training"][1])
    calibration_start = dates.index(config["splits"]["calibration"][0])
    evaluation_start = dates.index(config["splits"]["retrospective_evaluation"][0])
    evaluation_end = dates.index(config["splits"]["retrospective_evaluation"][1])
    return train_end, calibration_start, evaluation_start, evaluation_end


def baseline_records(rows: list[dict], config: dict, demo: bool):
    train_end, calibration_start, start, end = split_indices(rows, config, demo)
    all_records = backtest(rows, config["horizons"], calibration_start, end, train_end,
                           lookback=config["volatility"]["lookback"])
    warm = [r for r in all_records if calibration_start <= r["origin"] < start
            and r["origin"] + r["horizon"] < start]
    evaluation = [r for r in all_records if r["origin"] >= start]
    return warm, evaluation


def calibrate(warm: list[dict], evaluation: list[dict], config: dict,
              normalised: bool = True) -> list[dict]:
    output = []
    for model in sorted({r["model"] for r in evaluation}):
        for horizon in config["horizons"]:
            past = [r for r in warm if r["model"] == model and r["horizon"] == horizon]
            current = [r for r in evaluation if r["model"] == model and r["horizon"] == horizon]
            if not past or not current:
                raise ValueError("Each horizon needs warm calibration and evaluation predictions")

            def scale(row, h=horizon):
                return max(1e-8, row["origin_low"] * row["volatility"]
                           * math.sqrt(h)) if normalised else 1.0

            for alpha in config["intervals"]["alphas"]:
                for method in config["intervals"]["methods"]:
                    calibrator = SequentialCalibrator(
                        horizon, alpha, method, config["intervals"]["window"],
                        config["intervals"]["aci_gamma"])
                    for row in past:
                        calibrator.observe(
                            Residual(row["origin"], horizon,
                                     abs(row["actual"] - row["pred"]) / scale(row)),
                            now=current[0]["origin"], warm=True)
                    pending = []
                    for row in current:
                        now = row["origin"]
                        ready = [p for p in pending if p[0]["origin"] + horizon <= now]
                        for earlier, issued_q in ready:
                            calibrator.observe(
                                Residual(earlier["origin"], horizon,
                                         abs(earlier["actual"] - earlier["pred"]) / scale(earlier),
                                         issued_q), now=now)
                        pending = [p for p in pending if p[0]["origin"] + horizon > now]
                        q = calibrator.threshold(now)
                        width = q * scale(row)
                        lower, upper = row["pred"] - width, row["pred"] + width
                        score = 2 * width
                        if row["actual"] < lower:
                            score += 2 / alpha * (lower - row["actual"])
                        elif row["actual"] > upper:
                            score += 2 / alpha * (row["actual"] - upper)
                        output.append({**row, "method": method, "alpha": alpha,
                                       "normalisation": "volatility" if normalised else "absolute",
                                       "lower": lower, "upper": upper,
                                       "hit": int(lower <= row["actual"] <= upper),
                                       "interval_score": score, "alpha_used": calibrator.alpha_t,
                                       "feedback_count": len(calibrator.seen) - len(past)})
                        pending.append((row, q))
    return output


def run_stage(stage: str, dataset: str) -> Path:
    if stage == "B":
        raise ValueError("Stage B awaits an audited attention export; it has not been run")
    folder, rows, config = begin_run(stage, dataset)
    warm, evaluation = baseline_records(rows, config, dataset == "DEMO")
    write_csv(folder / "point_predictions.csv", evaluation)
    write_csv(folder / "point_metrics.csv", summarise(evaluation))
    if stage in {"C", "D"}:
        intervals = calibrate(warm, evaluation, config)
        if stage == "D":
            intervals += calibrate(warm, evaluation, config, normalised=False)
        write_csv(folder / "intervals.csv", intervals)
    metadata = json.loads((folder / "run.json").read_text())
    metadata["status"] = "completed_demo" if dataset == "DEMO" else "completed_baseline_only"
    metadata["attention_compared"] = False
    metadata["enbpi_compared"] = False
    metadata["proposed_adaptation_compared"] = False
    (folder / "run.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    return folder
