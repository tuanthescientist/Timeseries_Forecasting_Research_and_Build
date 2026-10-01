# Synthetic benchmark results

**Purpose:** verify that the evaluation pipeline runs and saves inspectable forecasts.
These are synthetic-data results, not Bitcoin, BNB, VN30, or gold performance estimates.

Run from the repository root:

```bash
ts-benchmark --csv data/demo/synthetic_prices.csv --output results/local/demo
```

Configuration: 600 observations, 12 common origins, spacing 7 observations, direct
horizons 1/7/30, expanding training history, ridge alpha 10. Recorded environment:
Python 3.11.9 and NumPy 2.2.6. See [run metadata](run.json) for hashes and parameters.

| Horizon (observations) | Model | MAE | RMSE | MAPE (%) |
| --- | --- | ---: | ---: | ---: |
| 1 | Naive | 1.0784 | 1.6069 | 0.6633 |
| 1 | Drift | 1.0812 | 1.6012 | 0.6660 |
| 1 | Ridge returns | 1.1290 | 1.6309 | 0.6954 |
| 7 | Naive | 3.4102 | 3.8842 | 2.1030 |
| 7 | Drift | 3.2868 | 3.9965 | 2.0337 |
| 7 | Ridge returns | 3.4432 | 4.0651 | 2.1329 |
| 30 | Naive | 4.7031 | 5.6782 | 2.8900 |
| 30 | Drift | 5.2499 | 6.4881 | 3.2629 |
| 30 | Ridge returns | 5.6571 | 7.0737 | 3.5204 |

Ridge does not outperform the simple baselines in this demonstration. This is retained
as observed, rather than selecting a generator or tuning parameters to advertise a win.
Model rankings on this constructed series should not be generalized to markets.

[Full-precision metrics](metrics.csv) and [all 108 predictions](predictions.csv) support
independent checks. Errors from overlapping horizons are dependent; no confidence
intervals or significance tests are reported.
