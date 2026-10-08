"""Generate deterministic synthetic OHLCV data with volatility clustering.

The series is artificial (GARCH(1,1)-style returns) and unrelated to any market. It lets
notebooks and CI run the full pipeline without redistributing provider data.
"""

from __future__ import annotations

import csv
from pathlib import Path

import numpy as np
import pandas as pd

ROWS = 3200
SEED = 7


def make_ohlcv(rows: int = ROWS, seed: int = SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    omega, a, b = 2e-6, 0.08, 0.90
    variance = omega / (1 - a - b)
    close = 1000.0
    out = []
    dates = pd.bdate_range("2005-01-03", periods=rows)
    for date in dates:
        sigma = np.sqrt(variance)
        gap = rng.normal(0, 0.3 * sigma)
        ret = rng.normal(0, sigma)
        open_ = close * np.exp(gap)
        new_close = close * np.exp(gap + ret)
        spread = abs(rng.normal(0, 0.6 * sigma))
        high = max(open_, new_close) * np.exp(spread)
        low = min(open_, new_close) * np.exp(-abs(rng.normal(0, 0.6 * sigma)))
        volume = 1e6 * np.exp(rng.normal(0, 0.3) + 20 * sigma)
        out.append((date.date().isoformat(), new_close, open_, high, low, volume))
        variance = omega + a * (gap + ret) ** 2 + b * variance
        close = new_close
    return pd.DataFrame(out, columns=["ds", "y", "open", "high", "low", "volume"])


def main() -> None:
    path = Path(__file__).resolve().parents[1] / "data/demo/synthetic_ohlcv.csv"
    frame = make_ohlcv()
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(frame.columns)
        for row in frame.itertuples(index=False):
            writer.writerow([row.ds] + [f"{v:.4f}" for v in row[1:5]] + [f"{row.volume:.0f}"])
    print(f"Wrote {len(frame)} synthetic OHLCV rows to {path.name}")


if __name__ == "__main__":
    main()
