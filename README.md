# BTC Forecasting and Interval Calibration

**Research question:** How do forecast horizon, volatility change and delayed feedback affect the accuracy and uncertainty of BTC-USD daily-Low forecasts?

The project develops an auditable evaluation protocol around one instrument and one target. Maintained by [Tuan Tran](https://github.com/tuanthescientist). The original TensorFlow attention notebook provides practical preparation; Stage A now reports simple baseline evidence; neural and interval comparisons remain pending.

| Component | Current status |
| --- | --- |
| Original BTC notebook | Archived unchanged; saved MAPE 3.40% concerns 30 rolling one-step predictions |
| BTC snapshot | New snapshot locked: 4,404 dates through 2026-10-07; original bytes remain unavailable |
| Protocol and temporal checks | Foundation design, four horizons: 1, 5, 20, 30 |
| Offline implementation | Persistence/drift, static/rolling/ACI, train-only regimes and basic comparisons |
| Attention / ETS-ARIMA / EnbPI / proposed method | Audited comparison or implementation pending |
| BTC research results / prospective evidence | Stage A baseline completed; B–D and future evaluation pending |

The saved 3.40% is not a 30-step forecast from one origin. The notebook's recursive future path holds other features fixed and is not scored by that metric. New code and synthetic checks do not certify those historical numbers or establish model superiority.

**Read:** [proposal](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/docs/proposal.md) → [protocol](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/docs/protocol.md) → [registration status](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/docs/preregistration.md) → [data card](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/docs/data_card.md). See the [original notebook](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/notebooks/archive/btc-low-forecast-tensorflow.ipynb), [decisions](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/tree/main/docs/decisions) and [bibliography](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/docs/references.bib).

## Reproduce the foundation

    python -m pip install -c requirements-lock.txt -e ".[dev]"
    python -m unittest discover -s tests -v
    python scripts/check_repository.py
    python scripts/smoke_demo.py

CI uses only synthetic data and no downloads, neural fitting or archived notebook execution. To restore the locked local Yahoo snapshot, install the acquisition extra and explicitly run:

    python -m pip install -e ".[acquisition]"
    python scripts/acquire_btc_snapshot.py --restore

Restoration requires an exact hash match and preserves the published manifest. The raw BTC CSV remains local. Changes to the acquisition request or full model specification require a versioned amendment before evaluation.

## Layout and next milestones

configs/ and data/manifest.json record the task and snapshot identity. src/btcforecast/ contains offline foundations; experiments/ separates stages A–E. notebooks/ reads saved artifacts; results/runs/ records individual runs and results/tables/ holds reviewed research tables. docs/proposal.md is the sole active proposal source; Word is an export, not a second editable proposal.

Next: freeze the attention/features specification, run and audit retrospective stages B–D (Stage A baseline completed), then reserve eligible future observations. The active protocol-v1.1 tag locks **foundation design**; the original protocol-v1 remains preserved. A full-study freeze is still pending. If A–D are not frozen before the proposed future start, publish an amendment with a new future window.

[Legacy portfolio](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/legacy/README.md) retains VN30, BID, supplementary code/results; vendor CSVs are now local only on main. These assets provide historical preparation and are excluded from BTC research claims. Cite [CITATION.cff](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/CITATION.cff) with the exact commit.

[Amendment 001](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/docs/amendments/amendment-001.md): bridge 2026-10-01–2027-01-31; candidate future window 2027-02-01–2027-07-30, conditional on a complete A–D freeze. [Audit](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/docs/audit-2026-10-08.md). Legacy CSV removal does not purge earlier Git history.

[Stage A results](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/results/tables/README.md): persistence MAE USD 1,309.84 at h=1 and USD 8,176.55 at h=30; log drift has higher MAE at all four horizons. This is retrospective baseline evidence, without a neural comparison or significance claim.
