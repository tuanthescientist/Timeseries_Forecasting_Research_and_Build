import math
import unittest

from btcforecast.conformal import Residual, SequentialCalibrator
from btcforecast.evaluation import backtest, eligible_labels
from btcforecast.models import load_attention_predictions


class NoLookaheadTests(unittest.TestCase):
    def test_delayed_feedback_boundary_for_every_horizon(self):
        for horizon in (1, 5, 20, 30):
            with self.subTest(horizon=horizon):
                calibrator = SequentialCalibrator(horizon, 0.2)
                residual = Residual(100, horizon, 4.0)
                with self.assertRaisesRegex(ValueError, "not observable"):
                    calibrator.observe(residual, now=100 + horizon - 1, warm=True)
                self.assertEqual(calibrator.pool, [])
                calibrator.observe(residual, now=100 + horizon, warm=True)
                self.assertEqual(len(calibrator.pool), 1)

    def test_warm_start_cannot_hide_unrealised_labels(self):
        calibrator = SequentialCalibrator(30, 0.2)
        with self.assertRaises(ValueError):
            calibrator.observe(Residual(90, 30, 1), now=100, warm=True)

    def test_cannot_mix_horizons_or_repeat_feedback(self):
        calibrator = SequentialCalibrator(5, 0.2)
        with self.assertRaises(ValueError):
            calibrator.observe(Residual(0, 1, 1), now=5)
        residual = Residual(0, 5, 1)
        calibrator.observe(residual, now=5, warm=True)
        with self.assertRaises(ValueError):
            calibrator.observe(residual, now=6, warm=True)

    def test_label_filter_includes_exact_availability_boundary(self):
        self.assertEqual(eligible_labels([0, 1, 2, 3], 5, 7), [0, 1, 2])

    def test_future_price_changes_do_not_change_origin_prediction_or_scale(self):
        rows = [{"date": str(i), "low": 100 + i * 0.2 + math.sin(i)} for i in range(160)]
        changed = [dict(row) for row in rows]
        for i in range(102, len(changed)):
            changed[i]["low"] *= 1000
        before = backtest(rows, [1, 5, 20, 30], 100, 159, 80)
        after = backtest(changed, [1, 5, 20, 30], 100, 159, 80)
        for a, b in zip(before, after, strict=True):
            if a["origin"] <= 101:
                for field in ("pred", "volatility", "regime", "mase_scale"):
                    self.assertEqual(a[field], b[field])

    def test_attention_adapter_rejects_future_training_labels(self):
        import csv
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "predictions.csv"
            row = {"origin": 10, "horizon": 5, "pred": 100, "information_end": 10,
                   "trained_label_end": 11, "selected_through": 5,
                   "protocol_sha256": "expected", "strategy": "direct"}
            with path.open("w", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=list(row))
                writer.writeheader()
                writer.writerow(row)
            with self.assertRaisesRegex(ValueError, "future"):
                load_attention_predictions(path, [{"low": 100}] * 30,
                                           protocol_sha256="expected")
