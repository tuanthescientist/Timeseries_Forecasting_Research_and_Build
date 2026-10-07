> Supplementary study documentation. This describes notebooks 01–03, not the three primary forecasting projects.

# Preliminary results

These figures are the committed run of notebooks 01–03, not a new experiment.
Result tables were produced at commit `7da3eb8` (7 October 2026). Later documentation
commits do not change them. Cite that commit, or a later one only after checking that
`results/vn30/` and `results/bid/` are unchanged.

This is a controlled comparison against persistence. It is not evidence of trading profit,
market efficiency, or a forecasting system that beats "no change".

## Protocol in one paragraph

Targets are 1-, 5- and 20-session log returns. An origin uses only data observed by that
row. Models refit every 20 origins. Hyper-parameters were chosen on a validation segment
and frozen before the test segment was scored. The test window starts on 3 January 2023
(912 origins on VN30, 905 on BID) and ends in August 2026. Differences from persistence
use a Diebold–Mariano test with HAC variance, a block bootstrap, and a Holm correction
within each dataset. Full rules: [protocol](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/docs/supplementary/protocol.md). Data limits: [data card](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/docs/supplementary/data.md).

## Point forecasts

RMSE of the predicted log return, divided by the RMSE of persistence on the same origins.
Below 1 would beat "no change".

| Series | Model | h = 1 | h = 5 | h = 20 |
| --- | --- | ---: | ---: | ---: |
| VN30 | trailing drift | 1.0023 | 1.0111 | 1.0415 |
| VN30 | ridge | 0.9976 | 0.9969 | 0.9718 |
| VN30 | extra-trees | 0.9974 | 0.9989 | 0.9736 |
| VN30 | gradient boosting | 0.9963 | 0.9965 | 1.0040 |
| BID | trailing drift | 1.0019 | 1.0084 | 1.0310 |
| BID | ridge | 0.9973 | 0.9897 | 0.9768 |
| BID | extra-trees | 0.9982 | 1.0011 | 1.0065 |
| BID | gradient boosting | 0.9961 | 1.0033 | 1.0155 |

No cell is distinguishable from persistence after Holm correction (adjusted p = 1 for all
24 model-by-horizon tests). The ridge ratio near 0.97 at h = 20 appears on both series and
is recorded as a lead for more assets, not as a finding. Source tables:
[VN30](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/results/vn30/02_test_point_metrics.csv),
[BID](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/results/bid/02_test_point_metrics.csv),
[VN30 tests](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/results/vn30/02_significance_vs_persistence.csv),
[BID tests](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/results/bid/02_significance_vs_persistence.csv).

## Interval coverage at h = 5

Empirical coverage on the test origins. Targets are 80% and 95%.

| Method | VN30 80% | VN30 95% | BID 80% | BID 95% |
| --- | ---: | ---: | ---: | ---: |
| Gaussian, EWMA volatility | 0.802 | 0.929 | 0.824 | 0.938 |
| Split conformal, static | 0.864 | 0.985 | 0.910 | 0.985 |
| Split conformal, rolling, volatility-normalised | 0.808 | 0.957 | 0.807 | 0.943 |
| Adaptive conformal, volatility-normalised | 0.799 | 0.948 | 0.798 | 0.947 |

Adaptive conformal is closest to the nominal level on average. Static intervals over-cover:
the 2018–2022 validation window was more volatile than the test years, so a quantile frozen
there is too wide later. Inside volatility terciles taken from the validation segment, the
same adaptive intervals at h = 5 and 80% cover about 0.71–0.74 of calm origins and about
0.87–0.93 of turbulent ones. Marginal calibration is therefore not conditional calibration.
That gap is the first doctoral experiment, not a completed method. Source:
[VN30](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/results/vn30/03_interval_summary.csv),
[BID](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/results/bid/03_interval_summary.csv).

## What these numbers do not support

* A claim that any learned model forecasts these series better than persistence.
* A claim that adaptive conformal is conditionally valid, or that the original coverage
  guarantee applies to the delayed-feedback update used here.
* Any statement about the four VN30 rows dated on weekends until those dates are reconciled
  with the exchange calendar. See [data card](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/docs/supplementary/data.md).
