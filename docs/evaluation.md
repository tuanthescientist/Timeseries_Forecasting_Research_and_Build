# Evaluation designs of the primary notebooks

The three primary notebooks are independent projects. They share forecasting concepts, not a single target, calendar, model-selection rule or final test. The supplementary protocol does not govern their original saved outputs.

| Project | Information at each origin | Reported evaluation | Main interpretation limit |
| --- | --- | --- | --- |
| VN30 / NeuralProphet | Historical price rows before the final 30 weekday rows | One direct 30-step prediction, raw and postprocessed | Smoothing is chosen using the reported outcomes; holidays are filled on a weekday grid. |
| BTC Low / TensorFlow | A 180-day window ending the previous day; actual test rows enter only after their day | Thirty one-step predictions from a fixed trained model | No independent validation split or baseline in the saved run; recursive future accuracy is unmeasured. |
| BID / ExtraTrees | Causal price/volume features and labels observed before each origin | Eight validation windows and three 30-step test windows, with zero-return baseline | Previously inspected history; three test windows; final-window MAPE is not the overall result. |

## What the metrics establish

MAE, RMSE and price MAPE describe the errors on the recorded segments. They do not by themselves establish that a model beats persistence, predicts direction well, generalises across regimes, or produces profitable trades. The BID notebook already provides a direct baseline comparison; the other two need one under their own forecast origins.

## Next evaluation before a stronger research claim

1. Record the source, retrieval date, adjustment policy, calendar, rights and hash of each market snapshot.
2. Specify the target and forecast origin: one-step updated daily, direct multi-step, or recursive multi-step. Compare models only on matching tasks.
3. Add persistence and simple drift baselines at identical origins.
4. Select smoothing and all other hyperparameters on chronological validation windows; freeze them before evaluating a new future window.
5. Report all windows, per-horizon errors, seed variability and regime-specific performance. Distinguish training diagnostics from held-out errors.
6. Evaluate interval coverage and width as a new experiment before presenting uncertainty claims for the primary projects.

These are proposed improvements, not changes to the saved model results. The original project code and outputs remain visible. The [supplementary study](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/docs/supplementary/README.md) contains optional evaluation infrastructure; its tests do not certify the primary notebooks.
