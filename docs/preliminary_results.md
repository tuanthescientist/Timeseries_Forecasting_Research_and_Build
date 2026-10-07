# Saved results from the three primary notebooks

These numbers come from the original notebook outputs supplied for this portfolio. Publication edits retain the predictions, tables, charts and metric outputs. No primary model was retrained to produce this page. The three tasks are not a common benchmark.

## VN30 / NeuralProphet

The saved run loads 4,408 source rows through 4 September 2026, reindexes to 4,610 weekday rows and evaluates a direct 30-step forecast on 27 July–4 September 2026. The training segment ends 24 July. Holiday gaps are filled.

| Forecast | MAPE (%) | MAE (index points) | RMSE (index points) |
| --- | ---: | ---: | ---: |
| Raw | 9.72 | 187.88 | 218.17 |
| Anchored and smoothed | 5.75 | 111.63 | 138.13 |

The notebook searches smoothing parameters by a discrete grid and Powell refinement **using the same final 30 outcomes**. The 3.97 percentage-point reduction is a retrospective tuning result. The smoothed MAPE does not estimate performance on an untouched future window. No persistence comparison is recorded in this saved evaluation.

Source: [NeuralProphet notebook](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/notebooks/vn30-forecast-neuralprophet.ipynb), backtest and raw/smoothed metric cells.

## Bitcoin Low / TensorFlow

The saved Yahoo Finance run contains 4,397 raw daily rows through 30 September 2026 and 4,368 feature-complete rows. The split is 4,338 training rows and 30 test rows. A 180-day input window produces 30 **one-step** predictions; each next window includes the previous day's realised observations. The model is not refitted during this test loop.

| Target | MAPE (%) | MAE (USD) | RMSE (USD) |
| --- | ---: | ---: | ---: |
| BTC-USD daily Low, final 30 days | 3.40 | 2,702.68 | 3,138.98 |

Scaler fitting uses only training rows. The model's early stopping and learning-rate reduction monitor training loss, with no independent validation split in this run. The later cell labelled Backtest predicts training windows and is an in-sample diagnostic. No persistence comparison or across-seed uncertainty is recorded for the held-out segment.

The future 30-day recursive forecast holds non-Low features constant; its accuracy is not measured by the table above. Live downloads, package versions and random training can change the result on rerun.

Source: [TensorFlow notebook](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/notebooks/btc-low-forecast-tensorflow.ipynb), split, windowing, training and evaluation cells.

## BID / scikit-learn ExtraTrees

The saved run has 3,153 rows through 24 September 2026. Five configurations are checked on eight validation windows. The chosen model uses a 1,512-observation training window, minimum leaf size 12, joint 30-step targets, half-life 252 and robust limit 3. It is evaluated at three consecutive 30-observation test windows.

| Test origin (row index) | Model | MAPE (%) | MAE (quoted price units) |
| --- | --- | ---: | ---: |
| 3063 | ExtraTrees | 3.197 | 1,247.859 |
| 3063 | Zero-return baseline | 2.269 | 886.687 |
| 3093 | ExtraTrees | 6.691 | 2,324.278 |
| 3093 | Zero-return baseline | 7.260 | 2,522.520 |
| 3123 | ExtraTrees | 1.229 | 445.702 |
| 3123 | Zero-return baseline | 1.128 | 407.593 |
| Three-window mean | ExtraTrees | **3.706** | **1,339.280** |
| Three-window mean | Zero-return baseline | **3.552** | **1,272.267** |

ExtraTrees mean daily direction accuracy is 38.889%, balanced direction accuracy 42.839%, and composite selection loss 0.968 versus the baseline's 1.000. A lower composite loss and a lower price MAPE measure different outcomes. ExtraTrees improves price MAPE in one window and is worse in two, including the final window. The printed 1.23% is the rounded final-window 1.229%.

History was inspected in earlier experiments, as the original notebook states. Validation-based selection inside this run does not make the full history a pristine prospective test. The notebook also flags an OHLC inconsistency and a missing September date for source verification. No trading-profit claim follows from these results.

Source: [ExtraTrees notebook](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/notebooks/stock-forecast-sklearn.ipynb), frozen configuration, test comparison table and scope notes.

## Relationship to the supplementary study

The numbered notebooks use their own snapshots, 1/5/20-observation return horizons and evaluation protocol. Their aggregate files in results/vn30/ and results/bid/ are **not** the source of the three primary projects' scores. They are documented separately in [supplementary results](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/docs/supplementary/preliminary_results.md).

See [evaluation designs](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/docs/evaluation.md) and [data provenance](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/docs/data.md) for what must be fixed before making a generalisation claim.
