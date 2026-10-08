import math
import unittest

from btcforecast.regimes import RegimeThresholds


class RegimeTests(unittest.TestCase):
    def test_suffix_and_future_append_cannot_change_training_thresholds(self):
        prices = [100 + i * 0.1 + math.sin(i / 3) for i in range(200)]
        fitted = RegimeThresholds.fit(prices, train_end=99)
        changed = prices[:100] + [1e8 * (i + 1) for i in range(100)]
        self.assertEqual(fitted, RegimeThresholds.fit(changed, train_end=99))
        self.assertEqual(fitted, RegimeThresholds.fit(prices + [1e12], train_end=99))

    def test_thresholds_do_respond_to_training_change(self):
        prices = [100 + math.sin(i / 3) for i in range(200)]
        before = RegimeThresholds.fit(prices, 99)
        prices[75] *= 2
        self.assertNotEqual(before, RegimeThresholds.fit(prices, 99))

    def test_boundary_classification_is_defined(self):
        fitted = RegimeThresholds(0.1, 0.2, 99)
        self.assertEqual(fitted.classify(0.1), "low")
        self.assertEqual(fitted.classify(0.2), "medium")
        self.assertEqual(fitted.classify(0.3), "high")
