import unittest

try:
    import numpy as np
    import pandas as pd

    from tsresearch.conformal import conformal_intervals, conformal_quantile, gaussian_intervals
    from tsresearch.metrics import (
        block_bootstrap_ci,
        coverage,
        diebold_mariano,
        directional_accuracy,
        holm_adjust,
        interval_score,
        loss_differential,
        pinball_loss,
        point_metrics,
    )
    HAVE_RESEARCH = True
except ImportError:
    HAVE_RESEARCH = False


@unittest.skipUnless(HAVE_RESEARCH, "research extras not installed")
class MetricTests(unittest.TestCase):
    def test_interval_score_and_pinball_known_values(self):
        # width 2, one miss below by 1 with alpha=0.1 -> 2 + (2/0.1)*1 = 22 ; other 2
        score = interval_score([0, 0], [2, 2], [-1, 1], alpha=0.1)
        self.assertAlmostEqual(score, (22 + 2) / 2)
        self.assertAlmostEqual(pinball_loss([1.0], [0.0], 0.9), 0.9)
        self.assertAlmostEqual(pinball_loss([0.0], [1.0], 0.9), 0.1)
        self.assertEqual(coverage([0, 0], [1, 1], [0.5, 2.0]), 0.5)

    def test_directional_accuracy_ignores_zero_forecasts(self):
        self.assertTrue(np.isnan(directional_accuracy([0, 0, 0], [1, -1, 1])))
        self.assertAlmostEqual(directional_accuracy([1, -1, 1, 1], [1, -1, -1, 0]), 2 / 3)

    def test_point_metrics_relative_to_persistence(self):
        rng = np.random.default_rng(0)
        actual = rng.normal(0, 0.01, 500)
        base = {"horizon": 1, "actual": actual, "price_target": 100 * np.exp(actual),
                "price_pred": np.full(500, 100.0)}
        frame = pd.concat([
            pd.DataFrame({**base, "model": "naive", "pred": np.zeros(500)}),
            pd.DataFrame({**base, "model": "oracle", "pred": actual})])
        table = point_metrics(frame, scale={1: 0.008}).set_index("model")
        self.assertAlmostEqual(table.loc["naive", "rel_rmse"], 1.0)
        self.assertAlmostEqual(table.loc["oracle", "rel_rmse"], 0.0)
        self.assertAlmostEqual(table.loc["naive", "mase"], np.mean(np.abs(actual)) / 0.008)

    def test_loss_differential_requires_identical_origins(self):
        frame = pd.DataFrame({"model": ["a", "a", "b"], "horizon": 1, "origin": [1, 2, 1],
                              "pred": 0.0, "actual": 1.0})
        with self.assertRaises(ValueError):
            loss_differential(frame, "a", "b", 1)

    def test_diebold_mariano_separates_real_differences_from_noise(self):
        rng = np.random.default_rng(1)
        noise = rng.normal(0, 1, 800)
        self.assertGreater(diebold_mariano(noise, 1)["p_value"], 0.01)
        shifted = noise - 0.5
        result = diebold_mariano(shifted, 1)
        self.assertLess(result["p_value"], 1e-6)
        self.assertLess(result["dm_stat"], 0)

    def test_dm_false_positive_rate_is_controlled_for_overlapping_errors(self):
        rng = np.random.default_rng(2)
        horizon, rejections, trials = 5, 0, 300
        for _ in range(trials):
            e = rng.normal(0, 1, 400 + horizon - 1)
            d = np.convolve(e, np.ones(horizon), mode="valid")  # MA(h-1) dependence
            rejections += diebold_mariano(d, horizon)["p_value"] < 0.05
        self.assertLess(rejections / trials, 0.10)

    def test_holm_adjustment(self):
        adjusted = holm_adjust([0.01, 0.04, 0.03])
        np.testing.assert_allclose(adjusted, [0.03, 0.06, 0.06])
        self.assertTrue((holm_adjust([0.5, 0.9]) <= 1).all())

    def test_block_bootstrap_interval_covers_the_mean(self):
        rng = np.random.default_rng(3)
        d = rng.normal(0.2, 1.0, 600)
        lo, hi = block_bootstrap_ci(d, block=10, n_boot=500, seed=1)
        self.assertLess(lo, d.mean())
        self.assertGreater(hi, d.mean())
        self.assertLess(hi - lo, 0.5)


@unittest.skipUnless(HAVE_RESEARCH, "research extras not installed")
class ConformalTests(unittest.TestCase):
    def make(self, n=3000, shift_at=None, factor=3.0, seed=4):
        rng = np.random.default_rng(seed)
        sigma = np.ones(n)
        if shift_at:
            sigma[shift_at:] = factor
        actual = rng.normal(0, sigma)
        return np.arange(n), np.zeros(n), actual, sigma

    def test_quantile_is_finite_sample_corrected(self):
        scores = np.arange(1, 11, dtype=float)
        self.assertEqual(conformal_quantile(scores, 0.9), 10.0)
        self.assertEqual(conformal_quantile(scores, 1.0), 10.0)
        self.assertEqual(conformal_quantile(scores, 0.0), 0.0)
        with self.assertRaises(ValueError):
            conformal_quantile(np.array([]), 0.9)

    def test_rolling_conformal_reaches_nominal_coverage(self):
        origin, pred, actual, _ = self.make()
        warm = np.abs(np.random.default_rng(9).normal(0, 1, 500))
        lo, hi, _ = conformal_intervals(origin, pred, actual, np.ones(len(origin)), 1, 0.1, warm,
                                        method="rolling", window=500)
        self.assertAlmostEqual(coverage(lo, hi, actual), 0.9, delta=0.02)

    def test_aci_recovers_coverage_after_a_variance_shift_that_static_misses(self):
        origin, pred, actual, _ = self.make(shift_at=1000)
        warm = np.abs(np.random.default_rng(9).normal(0, 1, 500))
        scale = np.ones(len(origin))
        covs = {}
        for method in ("static", "aci"):
            lo, hi, _ = conformal_intervals(origin, pred, actual, scale, 1, 0.1, warm,
                                            method=method, window=300, gamma=0.02)
            covs[method] = coverage(lo[1100:], hi[1100:], actual[1100:])
        self.assertLess(covs["static"], 0.6)
        self.assertGreater(covs["aci"], 0.85)

    def test_calibration_never_uses_outcomes_that_are_not_yet_realised(self):
        origin, pred, actual, _ = self.make(n=400)
        warm = np.abs(np.random.default_rng(9).normal(0, 1, 200))
        scale = np.ones(400)
        horizon, j = 20, 150
        corrupted = actual.copy()
        corrupted[j] = 1e6
        for method in ("rolling", "aci"):
            a = conformal_intervals(origin, pred, actual, scale, horizon, 0.1, warm, method)
            b = conformal_intervals(origin, pred, corrupted, scale, horizon, 0.1, warm, method)
            np.testing.assert_array_equal(a[0][: j + horizon], b[0][: j + horizon])
            np.testing.assert_array_equal(a[1][: j + horizon], b[1][: j + horizon])
            self.assertNotEqual(a[1][j + horizon], b[1][j + horizon])

    def test_gaussian_interval_width(self):
        lo, hi = gaussian_intervals([0.0], [2.0], 0.05)
        self.assertAlmostEqual(hi[0], 1.959964 * 2, places=5)
        self.assertAlmostEqual(lo[0], -hi[0])


if __name__ == "__main__":
    unittest.main()
