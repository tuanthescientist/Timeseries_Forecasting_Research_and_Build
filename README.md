# BTC Forecasting and Interval Calibration

**Research question:** How do forecast horizon, volatility change and delayed feedback affect the accuracy and uncertainty of BTC-USD daily-Low forecasts?

The project develops an auditable evaluation protocol around one instrument and one target. Maintained by [Tuan Tran](https://github.com/tuanthescientist). The original TensorFlow attention notebook provides practical preparation; a common benchmark and new calibration evidence are still to be produced.

| Component | Current status |
| --- | --- |
| Original BTC notebook | Archived unchanged; saved MAPE 3.40% concerns 30 rolling one-step predictions |
| BTC snapshot | Not acquired or locked; original download bytes cannot be recovered from saved outputs |
| Protocol and temporal checks | Foundation design, four horizons: 1, 5, 20, 30 |
| Offline implementation | Persistence/drift, static/rolling/ACI, train-only regimes and basic comparisons |
| Attention / ETS-ARIMA / EnbPI / proposed method | Audited comparison or implementation pending |
| BTC research results / prospective evidence | No results under this protocol |

The saved 3.40% is not a 30-step forecast from one origin. The notebook's recursive future path holds other features fixed and is not scored by that metric. New code and synthetic checks do not certify those historical numbers or establish model superiority.

**Read:** [proposal](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/research/btc-interval-calibration/docs/proposal.md) → [protocol](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/research/btc-interval-calibration/docs/protocol.md) → [registration status](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/research/btc-interval-calibration/docs/preregistration.md) → [data card](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/research/btc-interval-calibration/docs/data_card.md). See the [original notebook](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/research/btc-interval-calibration/notebooks/archive/btc-low-forecast-tensorflow.ipynb), [decisions](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/tree/research/btc-interval-calibration/docs/decisions) and [bibliography](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/research/btc-interval-calibration/docs/references.bib).

## Reproduce the foundation

    python -m pip install -c requirements-lock.txt -e ".[dev]"
    python -m unittest discover -s tests -v
    python scripts/check_repository.py
    python scripts/smoke_demo.py

CI uses only synthetic data and no downloads, neural fitting or archived notebook execution. To create a **new** local Yahoo snapshot later, install the acquisition extra and explicitly run:

    python -m pip install -e ".[acquisition]"
    python scripts/acquire_btc_snapshot.py

This updates acquisition evidence in data/manifest.json, not the frozen design. The raw BTC CSV remains local. Changes to the acquisition request or full model specification require a versioned amendment before evaluation.

## Layout and next milestones

configs/ and data/manifest.json record the task and snapshot identity. src/btcforecast/ contains offline foundations; experiments/ separates stages A–E. notebooks/ reads saved artifacts; results/runs/ records individual runs and results/tables/ holds reviewed research tables. docs/proposal.md is the sole active proposal source; Word is an export, not a second editable proposal.

Next: lock the snapshot, freeze the attention/features specification, run and audit retrospective stages A–D, then reserve eligible future observations. The protocol-v1 tag locks **foundation design**, not a completed model study. If A–D are not frozen before the proposed future start, publish an amendment with a new future window.

[Legacy portfolio](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/research/btc-interval-calibration/legacy/README.md) retains VN30, BID, supplementary code/results and the two published Investing.com CSVs. These assets provide historical preparation and are excluded from BTC research claims. Cite [CITATION.cff](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/research/btc-interval-calibration/CITATION.cff) with the exact commit.
