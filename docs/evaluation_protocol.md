# Evaluation protocol

## Available information

An origin `o` means that observations through `y[o]` are known. A horizon `h` predicts
`y[o+h]`. All horizons count rows, not elapsed calendar days. The input must be positive,
finite, chronological, and free of duplicate dates. The benchmark does not fill gaps.

The dataset is sliced at the origin inside `predict`, before constructing model inputs.
For a supervised row `t`, the label is `log(y[t+h]/y[t])`; it is included only if
`t+h <= o`. This also prevents multi-step training labels from crossing the boundary.

## Models

- **Naive:** predict the last observed price, `y[o]`.
- **Drift:** extrapolate `(y[o]-y[0])/o` by `h` observations. Prices are not clipped;
  negative drift forecasts are possible and should be inspected.
- **Ridge returns:** predict the direct `h`-step log return, then multiply the current
  price by its exponential. Features are log changes over 1, 2, 3, 7, 14, and 21 rows
  and standard deviations of one-step log returns over 7 and 21 rows (`ddof=0`).
  Features are standardized using only eligible training rows. The intercept is
  unpenalized; coefficients solve `(X.T X + alpha I) beta = X.T (r-mean(r))`.
  The fixed default `alpha=10` is illustrative and has not been tuned on market data.

Feature warm-up is 21 rows. The default requires at least 90 eligible training rows
at the earliest origin for the largest horizon. All available earlier history is used.
The supervised model has fewer eligible rows than the baseline history because it
requires warm-up and observed future labels.

## Rolling evaluation

Defaults are horizons 1, 7, 30; 12 origins spaced 7 observations apart. The last origin
is `n-1-max(horizons)`. Earlier origins move backward by `step`, then are evaluated in
chronological order. All models and horizons share the same origins. Models refit at
every origin; observations from earlier evaluation dates can become training data when
they have actually been observed. This is an expanding-window simulation.

The minimum row count is `min_train + 21 + 2*max(horizons) + (folds-1)*step` (248 with
the defaults). Each origin produces one prediction per horizon and model: 108 forecast
records in the default run. A 30-step forecast is one endpoint prediction, not an
average over a recursively predicted 30-day path.

## Reporting

MAE, RMSE, and MAPE are computed across origins separately for each model and horizon.
MAPE is multiplied by 100 and requires positive targets. No post-hoc adjustment uses
evaluation labels. Saved predictions make independent metric recomputation possible.

The run manifest records data and benchmark SHA-256, input date range, parameters,
Python version, and NumPy version. The benchmark is deterministic for a fixed input,
subject to floating-point differences. Use a Git commit to identify the full repository.

## Limits

The synthetic demo is a software demonstration, not a final holdout experiment. Twelve
origins provide little evidence for market-level conclusions. Forecast errors may be
dependent because horizons overlap. No statistical significance, uncertainty interval,
economic value, transaction cost, or trading strategy is evaluated. There is no nested
hyperparameter search or automatic validation/calibration stage; those must be designed
before a real-market comparison is reported.
