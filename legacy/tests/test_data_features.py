import tempfile
import unittest
from pathlib import Path

try:
    import numpy as np
    import pandas as pd

    from tsresearch.data import load_prices, quality_report
    from tsresearch.features import WARMUP, build_features, targets
    HAVE_RESEARCH = True
except ImportError:  # core-only environment
    HAVE_RESEARCH = False

EXPORT_CSV = '''Date,Price,Open,High,Low,Vol.,Change %
1/4/2021,"1,010.50","1,000.00","1,020.00","995.00",2.50M,1.05%
1/2/2021,1000.00,990.00,1005.00,985.00,"1,200",
1/3/2021,1004.00,1000.00,1000.00,1010.00,350K,0.40%
'''


@unittest.skipUnless(HAVE_RESEARCH, "research extras not installed")
class LoaderTests(unittest.TestCase):
    def write(self, text):
        handle = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8")
        handle.write(text)
        handle.close()
        self.addCleanup(Path(handle.name).unlink)
        return handle.name

    def test_export_layout_is_sorted_and_parsed(self):
        data = load_prices(self.write(EXPORT_CSV), "X")
        self.assertEqual(list(data.frame["ds"].dt.strftime("%Y-%m-%d")),
                         ["2021-01-02", "2021-01-03", "2021-01-04"])
        self.assertEqual(data.frame["y"].tolist(), [1000.0, 1004.0, 1010.5])
        self.assertEqual(data.frame["volume"].tolist(), [1200.0, 350e3, 2.5e6])
        self.assertEqual(len(data.sha256), 64)

    def test_quality_report_flags_inconsistent_ohlc_and_weekends(self):
        report = quality_report(load_prices(self.write(EXPORT_CSV), "X"))
        # 2021-01-02/03 are a Saturday and a Sunday; the 3rd row has high < low
        self.assertEqual(report["weekend_dated_rows"], 2)
        self.assertEqual(report["ohlc_inconsistent_rows"], 1)
        self.assertEqual(report["rows"], 3)

    def test_simple_ds_y_layout(self):
        data = load_prices(self.write("ds,y\n2020-01-01,5\n2020-01-02,6\n"))
        self.assertEqual(data.prices.tolist(), [5.0, 6.0])
        self.assertTrue(data.frame["open"].isna().all())

    def test_bad_input_is_rejected_not_repaired(self):
        for text in ("ds,y\n2020-01-01,5\n2020-01-01,6\n",
                     "ds,y\n2020-01-01,0\n",
                     "ds,y\n2020-01-01,abc\n",
                     "ds,y\nnot-a-date,5\n",
                     "a,b\n1,2\n"):
            with self.assertRaises(ValueError):
                load_prices(self.write(text))


@unittest.skipUnless(HAVE_RESEARCH, "research extras not installed")
class FeatureTests(unittest.TestCase):
    def setUp(self):
        from helpers import make_ohlcv
        frame = make_ohlcv(400, seed=3)
        frame["ds"] = pd.to_datetime(frame["ds"])
        frame["calendar_gap"] = frame["ds"].diff().dt.days.astype(float)
        self.frame = frame

    def test_features_use_only_past_and_present(self):
        base = build_features(self.frame)
        changed = self.frame.copy()
        changed.loc[250:, ["y", "open", "high", "low", "volume"]] *= 3.7
        altered = build_features(changed)
        pd.testing.assert_frame_equal(base.iloc[:250], altered.iloc[:250])
        self.assertFalse(base.iloc[250:].equals(altered.iloc[250:]))

    def test_targets_align_with_future_prices(self):
        prices = np.array([100.0, 110.0, 99.0, 120.0, 130.0])
        out = targets(prices, (1, 2))
        np.testing.assert_allclose(out[0], [np.log(1.1), np.log(0.99)])
        self.assertTrue(np.isnan(out[-1]).all())
        self.assertTrue(np.isnan(out[-2, 1]))
        self.assertFalse(np.isnan(out[-2, 0]))

    def test_warmup_is_positive(self):
        self.assertGreaterEqual(WARMUP, 60)


if __name__ == "__main__":
    unittest.main()
