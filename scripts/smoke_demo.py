"""Exercise only synthetic BTC-shaped data; no downloads, TensorFlow or saved results."""
import math

from btcforecast.data import verify_snapshot
from btcforecast.evaluation import summarise
from btcforecast.experiments import baseline_records, calibrate
from btcforecast.protocol import load_protocol

config, digest = load_protocol()
rows = verify_snapshot("DEMO")
warm, evaluation = baseline_records(rows, config, demo=True)
metrics = summarise(evaluation)
intervals = calibrate(warm, evaluation, config)
assert len(metrics) == 8
assert all(math.isfinite(row["mae"]) for row in metrics)
assert len(intervals) == len(evaluation) * 6
assert all(row["lower"] <= row["upper"] for row in intervals)
assert all(row["feedback_count"] >= 0 for row in intervals)
print(f"SYNTHETIC ONLY: {len(rows)} rows; {len(intervals)} interval records; protocol {digest}")
