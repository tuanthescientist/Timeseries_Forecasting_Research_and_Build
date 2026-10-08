# Active BTC evaluation protocol

The machine-readable authority is [configs/protocol.json](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/configs/protocol.json), version 1.1, with [Amendment 001](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/docs/amendments/amendment-001.md). Original protocol-v1 is preserved.

Forecast BTC-USD daily Low after UTC day t closes at horizons 1, 5, 20 and 30. A forecast uses observations through t only. Training: 2014-09-17–2021-12-31; validation: 2022-01-01–2023-06-30; calibration: 2023-07-01–2023-12-31; retrospective scoring: 2024-01-01–2026-09-30. Every scored endpoint must remain inside its stage. Preparation/bridge: 2026-10-01–2027-01-31, unscored. Future candidate: 2027-02-01–2027-07-30, conditional on full A–D freeze before its start.

Stage A compares persistence and 252-day log drift. Report MAE, RMSE, training-only MASE, relative MAE on paired persistence origins and secondary price MAPE. Stage B requires an audited attention export. C/D specify static, rolling and ACI intervals at 80% and 95%, separately by horizon, with absolute and causal volatility-normalised residuals. Only residuals with origin+h <= current origin may update calibration. Training-only volatility terciles define groups; groups under 100 observations are descriptive.

Primary future inference is ACI versus rolling normalised interval score across eight horizon/level comparisons, with Holm correction. Block bootstrap uses 30 days and sensitivity at 15/60 days; DM uses the amendment HAC rule and remains assumption-sensitive. Coverage diagnostics do not establish universal conditional coverage. These planned analyses have not all been executed.

Foundation scope blocks prospective scoring until a full-study amendment, valid freeze record and complete future outcomes exist. Missing a deadline requires a new future window. Never relabel retrospective observations as prospective.
