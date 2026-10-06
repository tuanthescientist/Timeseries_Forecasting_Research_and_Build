import tempfile
import unittest

try:
    import numpy as np
    import pandas as pd
    from helpers import make_ohlcv

    from tsresearch import models as models_module
    from tsresearch.backtest import run_backtest
    from tsresearch.data import Dataset
    from tsresearch.features import WARMUP
    from tsresearch.protocol import Protocol, segment_origins
    HAVE_RESEARCH = True
except ImportError:
    HAVE_RESEARCH = False


def make_dataset(rows=1100, seed=11):
    frame = make_ohlcv(rows, seed=seed)
    frame["ds"] = pd.to_datetime(frame["ds"])
    frame["calendar_gap"] = frame["ds"].diff().dt.days.astype(float)
    return Dataset("T", frame, "0" * 64, "synthetic")


def small_protocol(dataset):
    dates = dataset.dates
    return Protocol(validation_start=str(dates[500].date()), test_start=str(dates[800].date()),
                    horizons=(1, 5, 20), refit_every=20, min_train=300)


@unittest.skipUnless(HAVE_RESEARCH, "research extras not installed")
class SegmentTests(unittest.TestCase):
    def test_validation_targets_end_before_test_starts(self):
        data = make_dataset()
        protocol = small_protocol(data)
        origins = segment_origins(data.dates, protocol)
        test_start = origins["test"][0]
        self.assertLess(origins["validation"][-1] + protocol.max_horizon, test_start)
        self.assertEqual(origins["test"][-1] + protocol.max_horizon, len(data) - 1)
        self.assertGreaterEqual(origins["validation"][0], WARMUP + protocol.min_train)

    def test_empty_validation_is_rejected(self):
        data = make_dataset()
        bad = Protocol(validation_start="2009-01-01", test_start="2009-01-02", min_train=300)
        with self.assertRaises(ValueError):
            segment_origins(data.dates, bad)


@unittest.skipUnless(HAVE_RESEARCH, "research extras not installed")
class BacktestIntegrityTests(unittest.TestCase):
    SPECS = ({"family": "naive"}, {"family": "drift"}, {"family": "ridge", "alpha": 100.0},
             {"family": "extra_trees", "min_leaf": 40, "n_estimators": 20},
             {"family": "gradient_boosting", "max_iter": 20})

    def test_forecasts_ignore_everything_after_the_origin(self):
        data = make_dataset()
        protocol = small_protocol(data)
        cutoff = int(segment_origins(data.dates, protocol)["test"][0]) + 90
        altered_frame = data.frame.copy()
        altered_frame.loc[cutoff + 1:, ["y", "open", "high", "low", "volume"]] *= 5.0
        altered = Dataset("T", altered_frame, "1" * 64, "synthetic")
        for spec in self.SPECS:
            base = run_backtest(data, spec, protocol, "test")
            other = run_backtest(altered, spec, protocol, "test")
            keep = base["origin"] <= cutoff
            # multithreaded forests may differ in the last floating-point bits
            np.testing.assert_allclose(base.loc[keep, "pred"].to_numpy(),
                                       other.loc[keep, "pred"].to_numpy(),
                                       rtol=1e-8, atol=1e-12, err_msg=str(spec))
            self.assertFalse(np.array_equal(base["actual"], other["actual"]))

    def test_each_fit_sees_only_labels_observed_at_the_refit_origin(self):
        data = make_dataset()
        protocol = small_protocol(data)
        seen = []

        class Spy(models_module.Naive):
            def fit(self, X, Y, sample_weight=None):
                seen.append(len(Y))
                return self

        models_module.FAMILIES["spy"] = Spy
        self.addCleanup(models_module.FAMILIES.pop, "spy")
        run_backtest(data, {"family": "spy"}, protocol, "test")
        origins = segment_origins(data.dates, protocol)["test"]
        refit_origins = origins[::protocol.refit_every]
        expected = [int(o) - protocol.max_horizon - WARMUP + 1 for o in refit_origins]
        self.assertEqual(seen, expected)

    def test_cache_returns_identical_predictions(self):
        data = make_dataset()
        protocol = small_protocol(data)
        with tempfile.TemporaryDirectory() as tmp:
            first = run_backtest(data, self.SPECS[2], protocol, "validation", cache_dir=tmp)
            second = run_backtest(data, self.SPECS[2], protocol, "validation", cache_dir=tmp)
        np.testing.assert_allclose(first["pred"], second["pred"])
        self.assertEqual(len(first), len(second))

    def test_output_alignment(self):
        data = make_dataset()
        protocol = small_protocol(data)
        out = run_backtest(data, self.SPECS[0], protocol, "test")
        index = {d: i for i, d in enumerate(data.dates)}
        for row in out.sample(50, random_state=0).itertuples():
            self.assertEqual(index[row.target_date] - index[row.origin_date], row.horizon)
            self.assertAlmostEqual(row.actual, np.log(row.price_target / row.price_origin))
        self.assertTrue((out["pred"] == 0).all())


if __name__ == "__main__":
    unittest.main()
