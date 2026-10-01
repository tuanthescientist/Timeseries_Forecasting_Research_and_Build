"""Generate a deterministic synthetic positive series, unrelated to market data."""

import csv
import math
from datetime import date, timedelta
from pathlib import Path
import random


def main():
    rng = random.Random(42)
    path = Path(__file__).resolve().parents[1] / "data/demo/synthetic_prices.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    value = 100.0
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["ds", "y"])
        for i in range(600):
            drift = 0.0008 if i < 300 else -0.0002
            value *= math.exp(drift + 0.002 * math.sin(i / 10) + rng.gauss(0, 0.012))
            writer.writerow([(date(2020, 1, 1) + timedelta(days=i)).isoformat(), f"{value:.8f}"])
    print(f"Wrote 600 synthetic observations to {path.name}")


if __name__ == "__main__":
    main()
