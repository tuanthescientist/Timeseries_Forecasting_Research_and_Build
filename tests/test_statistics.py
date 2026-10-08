import unittest

from btcforecast.stats import block_bootstrap_mean, holm


class StatisticsTests(unittest.TestCase):
    def test_holm_known_example_preserves_original_order(self):
        result = holm([0.04, 0.001, 0.02])
        for actual, expected in zip(result, [0.04, 0.003, 0.04], strict=True):
            self.assertAlmostEqual(actual, expected)

    def test_bootstrap_is_seeded_and_contains_constant_mean(self):
        first = block_bootstrap_mean([2.0] * 100, block=10, samples=100, seed=42)
        self.assertEqual(first, (2.0, 2.0))
        self.assertEqual(first, block_bootstrap_mean([2.0] * 100, 10, 100, 42))

    def test_short_dependent_series_is_inconclusive(self):
        with self.assertRaises(ValueError):
            block_bootstrap_mean([1.0] * 10, block=30)
