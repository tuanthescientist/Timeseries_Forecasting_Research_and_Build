# Stage A — actual BTC baseline evidence

Run completed on 8 October 2026 under the published protocol-v1.1 design commit 7c769b8c. [Metrics](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/results/tables/stage_a_point_metrics.csv) and [provenance](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/results/tables/stage_a_run.json). Snapshot covers 4,404 dates; retrospective scoring is 2024-01-01–2026-09-30. Forecast endpoints stay within that period, so horizon sample counts differ.

| Horizon | Origins | Persistence MAE (USD) | Drift MAE (USD) | Drift / persistence MAE |
|---|---:|---:|---:|---:|
| 1 | 1003 | 1309.84 | 1310.51 | 1.0005 |
| 5 | 999 | 3225.03 | 3269.27 | 1.0137 |
| 20 | 984 | 6497.42 | 6942.84 | 1.0686 |
| 30 | 974 | 8176.55 | 9008.14 | 1.1017 |

Drift has higher MAE at all four horizons; this is a descriptive baseline comparison, not a significance claim. Persistence one-step price MAPE is 1.7106% over this period. Do not compare it directly with the archived attention 3.40% on only thirty different dates. MASE uses the fixed pre-2022 denominator and can be large after price/volatility changes.

Full per-origin prices/predictions remain local with artifact hashes in provenance. Raw vendor data is not redistributed. B–D and prospective results remain pending; this table does not establish a new method contribution.
