> Supplementary study documentation. This describes notebooks 01–03, not the three primary forecasting projects.

# Evaluation protocol

This is the single protocol used by all three notebooks. It is implemented in
[`src/tsresearch/`](../../src/tsresearch) and its integrity properties are unit-tested.
The dates below were fixed in [`configs/protocol.json`](../../configs/protocol.json) before
any model in this repository was run.

## Forecast target and information set

* One **observation** is one trading session. Horizons count observations (1, 5, 20), not
  calendar days.
* A forecast **origin** `t` means rows `0..t` are known. The target is the h-step log return
  `log(y[t+h] / y[t])`, one direct forecast per horizon. Price forecasts are
  `y[t] * exp(forecast)`.
* Features at row `t` are lagged returns, momentum, rolling volatility, an RSI, a trailing
  drift, and (where available and consistent) open/high/low/volume summaries. Rows whose OHLC
  values are missing or inconsistent are masked inside those features and flagged. Missing
  sessions are not imputed; `calendar_gap` exposes them.
* `tests/test_data_features.py` checks that altering any row after `t` leaves features at
  rows `<= t` unchanged.

## Segments

| Segment | Origins | Purpose |
| --- | --- | --- |
| train | before `validation_start` | model fitting only |
| validation | from `validation_start`, last origin `max(h)` rows before `test_start` | choose hyper-parameters; warm-start interval calibration |
| test | from `test_start` to the last origin with all horizons observable | frozen models, run once |

The `max(h)`-row embargo guarantees that no validation target overlaps the test period.
Test origins are consecutive observations (step 1), so their errors overlap and are
dependent (see "Inference").

| Dataset | Validation start | Test start |
| --- | --- | --- |
| VN30 | 2018-01-01 | 2023-01-01 |
| BID | 2019-01-01 | 2023-01-01 |

## Refitting and label availability

Models are refitted every 20 origins on an expanding window. A fit at origin `o` may use
training row `t` only if `t + max(h) <= o`, i.e. all of its labels were already observed.
Forecasts for the next 19 origins reuse that fit with their own causal features. A test in
`tests/test_backtest.py` verifies the number of training rows at every refit, and another
verifies that forecasts are unchanged when all data after the origin is replaced.

## Models

| Name | Description |
| --- | --- |
| `naive` | Persistence: zero expected log return |
| `drift` | Trailing 252-row mean return times `h` |
| `ridge` | Standardised features, ridge penalty `alpha` in {10, 100, 1000} |
| `extra_trees` | One multi-output forest, `min_samples_leaf` in {20, 60}; targets scaled by `sqrt(h)` |
| `gradient_boosting` | Histogram gradient boosting per horizon, `max_depth` in {2, 3} |

**Selection rule (validation only):** the score of a candidate is the mean over horizons of
its RMSE divided by persistence RMSE. The best candidate of each family is frozen. The
interval centre in notebook 03 is the best candidate overall, which may be persistence.

## Metrics

* `rel_rmse`, `rel_mae`: error divided by the persistence error on the same origins
  (`< 1` is better than persistence).
* `mase`: MAE divided by the in-sample mean absolute h-step return (training rows only).
* `direction_acc`: share of non-zero realised moves whose sign was forecast; undefined for
  persistence.
* `price_mape_pct`: price-level MAPE, reported for continuity but not used for selection.
* Intervals: empirical coverage, mean width, interval (Winkler) score, coverage by
  volatility regime and by calendar year.

## Inference

* **Diebold-Mariano** test on the squared-error differential, Bartlett HAC variance with `h-1`
  lags, Harvey-Leybourne-Newbold correction, Student-t reference.
* **Circular block bootstrap** (blocks of `max(20, 2h)`, 2000 resamples) for the mean loss
  difference.
* **Holm** correction across all model-by-horizon comparisons within a dataset.

## Interval calibration

For horizon `h`, the outcome of origin `j` is realised at `j + h` and may be used for
calibration at origin `k` only if `j + h <= k`. Validation scores are all realised before the
first test origin. `tests/test_metrics_conformal.py` verifies that corrupting an unrealised
outcome does not change any earlier interval.

* `static`: split conformal with validation scores, never updated.
* `rolling`: split conformal on the latest 500 realised scores.
* `aci`: adaptive conformal inference (Gibbs and Candès, 2021). With delayed feedback the
  update is a heuristic: coverage guarantees of the original algorithm are not claimed.
* Normalised variants divide residuals by `sigma_EWMA * sqrt(h)` (RiskMetrics decay 0.94).
