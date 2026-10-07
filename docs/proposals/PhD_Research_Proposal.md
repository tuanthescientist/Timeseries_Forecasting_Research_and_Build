# Calibrated Forecast Uncertainty under Regime Change

Proposed doctoral research · Trần Anh Tuân · 7 October 2026

A readable copy of the application text. The same text is in
[PhD_Research_Proposal_Tran_Anh_Tuan.docx](PhD_Research_Proposal_Tran_Anh_Tuan.docx).
Numbers below are the committed run; the tables live in
[preliminary results](../preliminary_results.md).

## Abstract

A useful forecast states a number and how much trust that number deserves when conditions
change. I propose to study prediction intervals for financial returns under volatility regime
change and, only after that result is stable, whether an evidence-checked report improves a
decision relative to the same numbers in a fixed template. A completed preliminary study on the
VN30 index and BIDV (BID), under a tested rolling-origin protocol, found that ridge regression,
extra-trees and gradient boosting do not beat persistence at a detectable level. Adaptive
conformal intervals kept marginal coverage within about one percentage point of the 80% and 95%
targets. Static calibration over-covered, and volatility-normalised intervals failed
conditionally: they under-covered calm periods and over-covered turbulent ones. The doctoral
project treats that negative point-forecast result as a baseline. The intended contribution is
a calibration method whose coverage holds inside regimes, not only on average, and a later
reporting layer that cannot state a number the evidence packet does not contain.

## 1. Problem

Inventory, staffing and risk limits depend on forecasts. For daily financial returns the hard
part is often not the point forecast. Persistence, a predicted log return of zero, is already
difficult to beat, and a small error in the price level can look like skill when it only
reflects that level. What remains useful is uncertainty that stays calibrated when volatility
shifts, and a report that does not add claims the numbers do not support.

The first empirical scope is daily VN30 and BID, where a protocol and a negative baseline
already exist. A public demand benchmark is a later domain. Energy, agriculture and weather
are out of scope. Realised trading profit is not an objective.

## 2. Related work and the gap

Accuracy is judged against a simple benchmark, with a scale-free metric such as MASE [1].
Diebold and Mariano [2], with the correction of Harvey, Leybourne and Newbold [3], test
whether a loss difference exceeds noise when errors are dependent. Rolling-origin evaluation,
not a random split, is the right design [4, 5]. M4 and M5 showed that rankings depend on the
loss, the horizon and the series, and that simple methods remain competitive [6, 7].

Distribution-free intervals need not assume that the whole sample is exchangeable.
Conformalised quantile regression [8], conformal prediction beyond exchangeability [9], EnbPI
[10] and conformal time-series forecasting [11] target marginal coverage under dependence or
weighted exchangeability. Adaptive conformal inference updates the miscoverage level online
when the distribution shifts [12]. Coverage alone is not enough: an interval score penalises
width, so a method cannot win by making every interval arbitrarily wide [13].

Pretrained time-series models transfer across datasets in zero-shot benchmarks [14, 15, 16].
Time-LLM reprograms a frozen language model to emit forecasts [17]. A direct ablation found
that, for point forecasting, removing the language-model component often did not hurt and
sometimes helped [18]. That is why this proposal does not treat a language model as a
forecasting engine. The open question is narrower: once a numerical forecast and an interval
exist, can a constrained report communicate them without unsupported numbers, and does that
communication change a decision [19]?

The gap is conditional coverage. Existing conformal methods are typically judged on marginal
coverage. The preliminary run shows that marginal coverage can sit on the nominal level while
coverage inside volatility regimes does not. The thesis studies horizon-specific sequential
calibration aimed at that failure, and only then a reporting layer whose numerical claims are
checked by code against an evidence packet available at the forecast origin.

## 3. Research questions

**RQ1.** Can sequential, horizon-specific calibration keep both marginal coverage and coverage
inside predefined volatility regimes when those regimes change, at a width that remains useful?
The working hypothesis is that adaptation reduces persistent over- or under-coverage relative
to a static split, but a volatility scale fitted on an earlier regime can over-correct.
Negative results will be reported.

**RQ2.** Can a schema, source timestamps and a deterministic numerical check reduce unsupported
statements relative to an unconstrained report, and does a verified report change cost in a
fixed inventory simulation relative to a template that shows the same forecast distribution?
The working hypothesis is that verification will cut unsupported numbers, while decision value
may be small once the numbers are already shown. The language model is not scored as a
forecaster [18].

These two questions are the thesis. Comparing further model families, including models from the
archived notebooks, is supporting work under the same protocol. A human study needs ethics
approval and is not required for the minimum thesis.

## 4. Preliminary evidence

The public repository implements the protocol and stores a completed run. Result tables are
those of commit `7da3eb8` (7 October 2026). Validation dates were fixed before that run. Models refit every 20
origins. A training label at horizon *h* is used only if it was already observed. Features at
an origin do not change if later prices are replaced. Those properties are unit-tested.

The test segment runs from 3 January 2023 into August 2026 (912 origins on VN30, 905 on BID).
Horizons are 1, 5 and 20 sessions. The table is RMSE of the log-return forecast divided by
persistence. Below 1 would beat "no change".

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

No comparison with persistence is significant after a Diebold–Mariano test with HAC variance,
a block bootstrap, and Holm correction (adjusted *p* = 1 in all 24 tests). A ridge ratio near
0.97 at horizon 20 appears on both series. With overlapping errors and one test window, that
is a lead for more data, not a result.

Empirical coverage at horizon 5:

| Method | VN30 80% | VN30 95% | BID 80% | BID 95% |
| --- | ---: | ---: | ---: | ---: |
| Gaussian, EWMA volatility | 0.802 | 0.929 | 0.824 | 0.938 |
| Split conformal, static | 0.864 | 0.985 | 0.910 | 0.985 |
| Rolling, volatility-normalised | 0.808 | 0.957 | 0.807 | 0.943 |
| Adaptive conformal, volatility-normalised | 0.799 | 0.948 | 0.798 | 0.947 |

Adaptive conformal is closest to the nominal level on average. Static intervals over-cover
because 2018–2022 was more volatile than the test years. Inside volatility terciles defined on
the validation segment, the normalised adaptive intervals at horizon 5 and 80% cover about
0.71–0.74 of calm origins and about 0.87–0.93 of turbulent ones. That conditional failure is
the starting point of RQ1.

Limits, so they are not discovered later: two series, one feature family, one test window,
and overlapping horizons. The delayed-feedback update does not inherit the coverage guarantee
of the original adaptive conformal algorithm. The same history was inspected informally before
the frozen run, so the test segment is not a never-seen sample. Provider, download date and
licence are unrecorded. Four VN30 test rows are dated Saturday or Sunday and must be
reconciled with the exchange calendar before any calendar claim. Market files are not in the
repository ([data card](../data.md), [results note](../preliminary_results.md)).

## 5. Proposed work

**RQ1.** Keep the existing protocol. On the validation segment only, fit a scale for interval
width: a monotone function of trailing EWMA volatility, or a quantile regression of the
absolute residual on volatility and horizon. Compare it with static split conformal, rolling
split conformal, an EnbPI-style ensemble where the compute budget allows, and adaptive
conformal inference [10, 12]. Report marginal coverage, coverage by predeclared volatility
regime, mean width and interval score. Freeze the scale and any step size before the test
segment is opened.

**RQ2, after a frozen interval exists.** The report receives an evidence packet: target,
origin time, forecast, interval, past errors, model disagreement, and allowed actions.
Context is admitted only if its timestamp is at or before the origin. Each numerical claim
needs an evidence identifier. Code checks every number against the packet; a failure falls
back to a fixed template. The model may not change the forecast. Scores are consistency,
unsupported-claim rate, abstention, and cost in an inventory simulation with fixed shortage
and holding costs. Hindsight is used only for scoring. A human study needs ethics approval.

Further model families enter only as a check that the interval result does not depend on the
centre. An LLM is not added to that comparison [18].

## 6. Data and evaluation rules

Before any new test run, the VN30 and BID cards will name the provider, the calendar, the
adjustment policy and the usage rights, or the series will not be used in a submitted result.
A second domain, if reached, will be a public licensed demand benchmark chosen before fitting,
with the series list fixed in advance. Horizons stay in observations, not calendar days.
Fit, selection, calibration and the final window are chronological. Overlapping targets are
separated by a gap at each boundary. A change of rule after the final window opens requires a
new prospective window.

Point metrics are MAE, RMSE and MASE, with the MASE denominator fitted before the test
segment. MAPE is secondary and is not used on returns. Interval metrics are coverage at 80%
and 95%, mean width, interval score, and pinball loss where the model emits a quantile.
Differences use a block bootstrap and a Diebold–Mariano test, with Holm correction inside each
family of tests. Failed fits and runtime are reported with the best cell, not instead of it.

## 7. Contribution, feasibility and plan

Three contributions are in view. The first is already in hand: an audited protocol and a
public negative result against persistence. The second is a calibration comparison aimed at
conditional coverage under a volatility shift, which marginal adaptive conformal did not
solve. The third is an evidence schema and a checker for forecast reports, scored against a
template that shows the same numbers. A useful outcome may be a boundary: a simpler interval,
or a template, is the better tool.

Preparation is a First Class Honours degree in Computing Science, a final-year project on café
revenue, and the repository above, with tests and continuous integration. Archived notebooks
are exploratory and are not cited as validated accuracy.

* Year 1. Confirm provenance and reconcile the weekend-dated VN30 rows. Complete the
  literature review against the list below. Run the conditional-coverage experiment on the
  existing protocol.
* Year 2. Repeat on at least one further asset and one stress window. Compare calibration
  methods. Keep the failures.
* Year 3. Verified reports, ablations, and the inventory simulation. A human study only if it
  is approved.
* Year 4. Replication, public artefacts, thesis.

The minimum thesis is RQ1 on the two series already in the protocol, plus the inventory
comparison in RQ2 if the report layer is stable. If conditional coverage does not improve,
that negative result is the finding, and the report layer is evaluated on the best simple
interval rather than dropped.

## 8. Reproducibility and use

Releases include code, a locked environment, split dates, prompts, schemas and verification
rules. Data are redistributed only if the provider allows; otherwise the card records the hash
and how to obtain the file. A retrospective language-model test can be contaminated by
pretraining, so that check will be prospective or will use a local model with a known cutoff.

This document is proposed work plus one preliminary study. It is not a finished doctorate, a
trading system, or an agreed supervision.

## References

1. Hyndman, R. J., and Koehler, A. B. (2006). Another look at measures of forecast accuracy. *International Journal of Forecasting*, 22(4), 679–688. https://doi.org/10.1016/j.ijforecast.2006.03.001
2. Diebold, F. X., and Mariano, R. S. (1995). Comparing predictive accuracy. *Journal of Business & Economic Statistics*, 13(3), 253–263. https://doi.org/10.1080/07350015.1995.10524599
3. Harvey, D., Leybourne, S., and Newbold, P. (1997). Testing the equality of prediction mean squared errors. *International Journal of Forecasting*, 13(2), 281–291. https://doi.org/10.1016/S0169-2070(96)00719-4
4. Tashman, L. J. (2000). Out-of-sample tests of forecasting accuracy: an analysis and review. *International Journal of Forecasting*, 16(4), 437–450. https://doi.org/10.1016/S0169-2070(00)00065-0
5. Bergmeir, C., and Benítez, J. M. (2012). On the use of cross-validation for time series predictor evaluation. *Information Sciences*, 191, 192–213. https://doi.org/10.1016/j.ins.2011.12.028
6. Makridakis, S., Spiliotis, E., and Assimakopoulos, V. (2020). The M4 Competition: 100,000 time series and 61 forecasting methods. *International Journal of Forecasting*, 36(1), 54–74. https://doi.org/10.1016/j.ijforecast.2019.04.014
7. Makridakis, S., Spiliotis, E., and Assimakopoulos, V. (2022). M5 accuracy competition: Results, findings, and conclusions. *International Journal of Forecasting*, 38(4), 1346–1364. https://doi.org/10.1016/j.ijforecast.2021.11.013
8. Romano, Y., Patterson, E., and Candès, E. (2019). Conformalized quantile regression. *Advances in Neural Information Processing Systems*, 32. https://arxiv.org/abs/1905.03222
9. Barber, R. F., Candès, E. J., Ramdas, A., and Tibshirani, R. J. (2023). Conformal prediction beyond exchangeability. *The Annals of Statistics*, 51(2), 816–845. https://arxiv.org/abs/2202.13415
10. Xu, C., and Xie, Y. (2021). Conformal prediction interval for dynamic time-series. *Proceedings of the 38th International Conference on Machine Learning*, PMLR 139, 11559–11569. https://arxiv.org/abs/2010.09107
11. Stankevičiūtė, K., Alaa, A. M., and van der Schaar, M. (2021). Conformal time-series forecasting. *Advances in Neural Information Processing Systems*, 34. https://proceedings.neurips.cc/paper/2021/hash/312f1ba2a72318edaaa995a67835fad5-Abstract.html
12. Gibbs, I., and Candès, E. (2021). Adaptive conformal inference under distribution shift. *Advances in Neural Information Processing Systems*, 34. https://arxiv.org/abs/2106.00170
13. Gneiting, T., and Raftery, A. E. (2007). Strictly proper scoring rules, prediction, and estimation. *Journal of the American Statistical Association*, 102(477), 359–378. https://doi.org/10.1198/016214506000001437
14. Ansari, A. F., Stella, L., Turkmen, C., Zhang, X., Mercado, P., Shen, H., Shchur, O., Rangapuram, S. S., Pineda Arango, S., Kapoor, S., Zschiegner, J., Maddix, D. C., Wang, H., Mahoney, M. W., Torkkola, K., Wilson, A. G., Bohlke-Schneider, M., and Wang, Y. (2024). Chronos: Learning the language of time series. *Transactions on Machine Learning Research*. https://arxiv.org/abs/2403.07815
15. Das, A., Kong, W., Sen, R., and Zhou, Y. (2024). A decoder-only foundation model for time-series forecasting. *Proceedings of the 41st International Conference on Machine Learning*, PMLR 235. https://arxiv.org/abs/2310.10688
16. Woo, G., Liu, C., Kumar, A., Xiong, C., Savarese, S., and Sahoo, D. (2024). Unified training of universal time series forecasting transformers. *Proceedings of the 41st International Conference on Machine Learning*, PMLR 235. https://arxiv.org/abs/2402.02592
17. Jin, M., Wang, S., Ma, L., Chu, Z., Zhang, J. Y., Shi, X., Chen, P.-Y., Liang, Y., Li, Y.-F., Pan, S., and Wen, Q. (2024). Time-LLM: Time series forecasting by reprogramming large language models. *International Conference on Learning Representations*. https://arxiv.org/abs/2310.01728
18. Tan, M., Merrill, M. A., Gupta, V., Althoff, T., and Hartvigsen, T. (2024). Are language models actually useful for time series forecasting? *Advances in Neural Information Processing Systems*, 37. https://arxiv.org/abs/2406.16964
19. Zhao, H., et al. (2025). TimeSeriesScientist: A general-purpose AI agent for time series analysis. arXiv preprint. https://arxiv.org/abs/2510.01538

Repository: https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build
