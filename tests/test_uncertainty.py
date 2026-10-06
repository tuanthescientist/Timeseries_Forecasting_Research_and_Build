import unittest

try:
    import numpy as np
    import pandas as pd

    from tsresearch.uncertainty import (
        METHODS,
        build_intervals,
        coverage_by_regime,
        summarise_intervals,
    )
    HAVE_RESEARCH = True
except ImportError:
    HAVE_RESEARCH = False


def fake_predictions(first_origin, n, horizon, seed):
    rng = np.random.default_rng(seed)
    vol = np.full(n, 0.01)
    origin = np.arange(first_origin, first_origin + n)
    return pd.DataFrame({
        "model": "m", "segment": "x", "horizon": horizon, "origin": origin,
        "origin_date": pd.date_range("2020-01-01", periods=n), "target_date": pd.NaT,
        "pred": 0.0, "actual": rng.normal(0, 0.01 * np.sqrt(horizon), n), "vol_ewma": vol})


@unittest.skipUnless(HAVE_RESEARCH, "research extras not installed")
class UncertaintyTests(unittest.TestCase):
    def setUp(self):
        self.validation = fake_predictions(0, 600, 5, 1)
        self.test = fake_predictions(700, 800, 5, 2)
        self.intervals = build_intervals(self.validation, self.test, alphas=(0.2,))

    def test_every_method_is_produced_on_identical_origins(self):
        self.assertEqual(set(self.intervals["method"]), set(METHODS))
        sizes = self.intervals.groupby("method").size()
        self.assertEqual(sizes.nunique(), 1)
        self.assertTrue((self.intervals["upper"] >= self.intervals["lower"]).all())

    def test_summary_coverage_is_close_to_nominal_for_stationary_data(self):
        summary = summarise_intervals(self.intervals)
        self.assertEqual(set(summary["nominal"]), {0.8})
        self.assertTrue((summary["coverage_gap"].abs() < 0.06).all())
        self.assertTrue((summary["interval_score"] > 0).all())

    def test_regime_table_has_three_regimes(self):
        table = coverage_by_regime(self.intervals, (0.0, 0.02))
        self.assertEqual(set(table["regime"]), {"mid vol"})
        table = coverage_by_regime(self.intervals, (0.1, 0.2))
        self.assertEqual(set(table["regime"]), {"low vol"})

    def test_rejects_mixed_models(self):
        mixed = pd.concat([self.test, self.test.assign(model="other")])
        with self.assertRaises(ValueError):
            build_intervals(self.validation, mixed)


if __name__ == "__main__":
    unittest.main()
