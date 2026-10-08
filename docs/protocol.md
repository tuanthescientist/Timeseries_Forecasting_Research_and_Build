# BTC foundation protocol v1

Design date: 8 October 2026. Author: Trần Anh Tuấn. Status: foundation design only.
Machine-readable decisions are in [protocol.json](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/research/btc-interval-calibration/configs/protocol.json);
[protocol-lock.json](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/research/btc-interval-calibration/configs/protocol-lock.json) records the canonical hash and
artifact hashes. The prior portfolio commit is eb1eac0.

## Instrument, target and information

BTC-USD from Yahoo Finance, with unadjusted daily OHLCV. The endpoint is daily **Low**,
not Close, FRED spot price or a tradable execution price. UTC day t must have closed
before its observation can be used. For each horizon h in 1, 5, 20 and 30, forecast
Low at t+h. Rolling one-step, direct and recursive strategies are distinct experiments.

The raw requested history spans 2014-09-17 through 2026-10-07 inclusive. Retrieval
has not occurred for the new protocol. A later download is a new snapshot with its
own timestamp and hash; it cannot recover the old notebook's exact input bytes.

## Chronological stages

| Stage | Dates | Permitted use |
| --- | --- | --- |
| Training | 2014-09-17–2021-12-31 | Initial model fitting, scaler and regime thresholds |
| Validation | 2022-01-01–2023-06-30 | Model/settings selection; no final-period tuning |
| Calibration | 2023-07-01–2023-12-31 | Initial residual pool; only realised labels |
| Retrospective evaluation | 2024-01-01–2026-09-30 | Frozen-rule evaluation; previously inspected history |
| Prospective candidate | 2026-10-09–2027-04-06 | Eligible only if required freezes occur before its start |

Every label must remain inside its stage when used for selection or initial calibration.
At current origin k, a residual from origin j enters calibration only when j+h ≤ k.
Horizons have separate pools. Model refits may use only fully realised labels. Predictions,
scalers, feature windows and regime assignments must use observations through the origin.

Earlier evaluation outcomes may update the calibrator under its declared prequential
rule; they never select settings or alter group definitions.

## Baselines, scales and intervals

Persistence predicts the last observed Low. Geometric drift extrapolates trailing
252 Low-to-Low log changes. The initial MASE denominator uses training-only one-day
absolute Low differences and stays fixed. Report MAE/RMSE/MASE and relative MAE
against persistence; price MAPE is secondary, and return-MAPE is excluded.

Static, rolling and ACI use absolute or volatility-normalised residuals. Normalisation
is origin Low × trailing 30-day Low-log-change volatility × square-root horizon,
floored at 1e-8. This scaling is an empirical approximation, not a distributional guarantee.
The rolling window is 500, ACI step size 0.005, and nominal coverage is 80% and 95%.

The empirical score rank is ceil((n+1) × level). Select that order statistic directly;
if it exceeds n, return an unbounded threshold. ACI feedback uses the threshold actually
issued for that forecast, not a newly calculated threshold.

Volatility terciles are fitted on training only. Report group counts; fewer than 100
observations makes a group inconclusive. Report coverage and interval score jointly
with width, by horizon, group and contiguous time block. Marginal, long-run and group
coverage are separate empirical quantities.

## Comparisons and remaining model decisions

The declared primary family compares normalised ACI versus normalised rolling interval
score across four horizons and two levels. Apply Holm within this eight-comparison family.
Use circular fixed-block bootstrap with 30-day blocks, 15/60 sensitivity, 1,000 draws,
seed 42. This code does not implement the stationary bootstrap.

DM uses matched loss series, at least max(50, 5h) origins, horizon-based HAC and a
small-sample correction. Kupiec/Christoffersen are secondary assumption-sensitive
diagnostics, not coverage guarantees under arbitrary financial dependence.

The active attention adapter validates exported cutoffs and protocol identity; it
does not train a new model. Exact features, training configuration and full competing
method implementations are pending. Freeze them in an amendment before claiming a
complete model comparison. EnbPI and a proposed adaptation are not implemented.

## Eligibility and amendments

The candidate future window is valid only if the design tag is published and snapshot,
attention specification and retrospective stages A–D are frozen before 2026-10-09.
Otherwise publish a dated amendment choosing a genuinely future start. Never relabel
already visible history as prospective or backdate a registration.

No new financial experiment is run by this restructuring. A protocol-v1 tag records a
foundation design and real publication event; it does not demonstrate that A–D are complete.
