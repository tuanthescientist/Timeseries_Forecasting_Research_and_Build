import math
import random
import unittest

from btcforecast.conformal import Residual, SequentialCalibrator, conformal_quantile


class ConformalTests(unittest.TestCase):
    def test_exact_rank_regression_for_historical_quantile_bug(self):
        self.assertEqual(conformal_quantile(list(range(1, 11)), 0.8), 9)
        self.assertEqual(conformal_quantile(list(range(1, 11)), 0.9), 10)

    def test_unattainable_rank_is_unbounded(self):
        self.assertTrue(math.isinf(conformal_quantile([1, 2, 3], 0.95)))
        self.assertTrue(math.isinf(conformal_quantile([1, 2], 1)))
        self.assertEqual(conformal_quantile([1, 2], 0), 0)

    def test_invalid_scores_rejected(self):
        for scores in ([], [-1], [math.nan], [math.inf]):
            with self.assertRaises(ValueError):
                conformal_quantile(scores, 0.8)

    def test_aci_uses_issued_threshold_not_new_threshold(self):
        calibrator = SequentialCalibrator(1, 0.2, "aci", gamma=0.1)
        for origin in range(20):
            calibrator.observe(Residual(origin, 1, 100), now=21, warm=True)
        # Current pool would cover 5; the previously issued q=1 missed it.
        calibrator.observe(Residual(21, 1, 5, issued_q=1), now=22)
        self.assertAlmostEqual(calibrator.alpha_t, 0.12)

    def test_static_ignores_new_scores_and_time_cannot_reverse(self):
        calibrator = SequentialCalibrator(1, 0.2, "static")
        for origin in range(20):
            calibrator.observe(Residual(origin, 1, 1), now=21, warm=True)
        before = calibrator.threshold(21)
        calibrator.observe(Residual(21, 1, 100), now=22)
        self.assertEqual(before, calibrator.threshold(22))
        with self.assertRaises(ValueError):
            calibrator.threshold(21)

    def test_monte_carlo_exchangeable_coverage_sanity_not_time_series_guarantee(self):
        rng = random.Random(123)
        hits = 0
        repetitions = 1000
        for _ in range(repetitions):
            scores = [abs(rng.gauss(0, 1)) for _ in range(99)]
            outcome = abs(rng.gauss(0, 1))
            hits += outcome <= conformal_quantile(scores, 0.8)
        self.assertTrue(0.75 <= hits / repetitions <= 0.85)
