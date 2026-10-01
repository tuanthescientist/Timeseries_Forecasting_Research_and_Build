import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

import numpy as np

from tsresearch.benchmark import evaluate, features, load_series, predict, training_indices


class BenchmarkTests(unittest.TestCase):
    def setUp(self):
        self.values = 100 * np.exp(np.arange(400) * 0.001 + 0.01 * np.sin(np.arange(400)))
        self.dates = [(date(2020, 1, 1) + timedelta(days=i)).isoformat() for i in range(400)]

    def test_future_changes_do_not_change_forecast(self):
        changed = self.values.copy()
        changed[301:] *= 100
        for horizon in (1, 7, 30):
            self.assertEqual(predict(self.values, 300, horizon), predict(changed, 300, horizon))
        np.testing.assert_array_equal(features(self.values, 300), features(changed, 300))

    def test_training_labels_do_not_cross_origin(self):
        for horizon in (1, 7, 30):
            indices = training_indices(300, horizon)
            self.assertTrue(np.all(indices + horizon <= 300))
            self.assertEqual(indices[-1] + horizon, 300)

    def test_constant_series_has_zero_error(self):
        predictions, metrics = evaluate(self.dates, np.full(400, 100.0))
        self.assertEqual(len(predictions), 108)
        for row in metrics:
            self.assertAlmostEqual(row["mae"], 0)
            self.assertAlmostEqual(row["rmse"], 0)
            self.assertAlmostEqual(row["mape_percent"], 0)

    def test_naive_and_drift_known_values(self):
        result = predict(np.arange(1, 401, dtype=float), 300, 7)
        self.assertEqual(result["naive"], 301)
        self.assertEqual(result["drift"], 308)

    def test_origin_target_alignment(self):
        predictions, _ = evaluate(self.dates, self.values)
        for row in predictions:
            origin = self.dates.index(row["origin"])
            target = self.dates.index(row["target_date"])
            self.assertEqual(target - origin, row["horizon"])
            self.assertEqual(row["actual"], self.values[target])

    def test_reject_short_data_and_invalid_configuration(self):
        with self.assertRaises(ValueError):
            evaluate(self.dates[:100], self.values[:100])
        for horizons in ((0,), (1, 1), ()):
            with self.assertRaises(ValueError):
                evaluate(self.dates, self.values, horizons=horizons)
        with self.assertRaises(ValueError):
            predict(self.values, 300, 1, alpha=0)

    def test_csv_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "series.csv"
            for content in (
                "ds,y\n2020-01-02,2\n2020-01-01,1\n",
                "ds,y\n2020-01-01,1\n2020-01-01,2\n",
                "ds,y\n2020-01-01,0\n",
                "ds,y\n2020-01-01,nan\n",
                "date,price\n2020-01-01,1\n",
            ):
                path.write_text(content, encoding="utf-8")
                with self.assertRaises(ValueError):
                    load_series(path)
            path.write_text("ds,y\n2020-01-01,12.5\n", encoding="utf-8")
            dates, values = load_series(path)
            self.assertEqual(dates, ["2020-01-01"])
            self.assertEqual(values[0], 12.5)


if __name__ == "__main__":
    unittest.main()
