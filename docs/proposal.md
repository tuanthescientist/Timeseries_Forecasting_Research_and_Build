# BTC Forecasting and Interval Calibration Under Delayed Feedback

Proposed doctoral research · Trần Anh Tuấn · 8 October 2026

## Abstract

I propose to study how forecast horizon, volatility change and delayed outcome availability affect BTC-USD daily-Low predictions and interval calibration. My original TensorFlow notebook supplies a concrete attention-based implementation and reports 3.40% MAPE for thirty rolling one-step predictions. It does not evaluate a thirty-step path from one origin, and its original downloaded bytes are unavailable. The new study therefore starts with a documented snapshot and a chronological protocol, then compares horizon strategies and established interval methods. Its methodological candidate combines horizon-specific residual histories with causal volatility scaling and explicit delayed updates. Existing methods and simple baselines may prove sufficient; negative findings will be retained. A new BTC snapshot is locked; baseline evidence is reported separately, with attention and interval comparisons pending.

## 1. Motivation and scope

Forecasts at horizons 1, 5, 20 and 30 have different information constraints. At origin t, an h-step error is unavailable until t+h. A calibrator that updates immediately with that error leaks future information. A method can also obtain acceptable average coverage while repeatedly missing outcomes during a volatile period.

The study fixes one instrument and one initial target: Yahoo Finance BTC-USD daily Low. The target is a reported daily-bar minimum, not an executable trading price. Low-to-Low changes define the initial volatility proxy. Close and FRED spot price require separately declared tasks. Keeping the initial scope narrow makes temporal assumptions, baseline comparisons and calibration feedback easier to audit.

## 2. Related work and bounded opportunity

Forecasting foundations [1], accuracy measures [2], out-of-sample evaluation [3] and evaluation pitfalls [4] motivate chronological selection, matching origins and serious baselines. Financial prediction studies [10, 11] show why simple benchmarks deserve attention, but their exchange-rate and equity-premium findings are not direct evidence about BTC Low.

The current preparation uses attention components [13]. NeuralProphet [12] and ExtraTrees [14] remain historical implementation experience in the legacy portfolio; they are not additional primary instruments in this study. Using attention is not itself a research contribution. Strategy, features and access to realised history must be controlled before interpreting model differences.

Predictive-accuracy comparison [5, 6], multiplicity control [7], dependent-data resampling [8] and model confidence sets [9] inform statistical assessment. The foundation implements a circular fixed-block bootstrap, not the stationary bootstrap in [8]. A larger model confidence set is optional; no significant superiority has been established.

Proper interval scoring [15] and conformalized quantile regression [16] motivate assessing coverage and width together. Conformal basics [17] clarify exchangeability assumptions. Limits of conditional inference [18] and extensions beyond exchangeability [19] prevent importing universal group-coverage guarantees into changing financial data.

ACI [20], its online extension [21], EnbPI [22] and adaptive aggregation [23] are relevant competitors. Their update mechanisms, score construction and assumptions differ. The bounded opportunity is to identify when horizon-dependent delay and changing volatility cause persistent miscoverage, then test whether a targeted adaptation improves coverage at a useful width. The distinction between marginal and group coverage is already known; novelty must go beyond restating it and be established with supervision.

## 3. Questions and hypotheses

**RQ1.** When do direct, recursive and rolling attention forecasts improve on persistence and drift under matching origins, targets and information sets?

**H1.** Some apparent price accuracy will disappear relative to simple baselines after matching the task and selecting settings on independent chronological validation. Evidence will use per-origin losses at fixed horizons and report all periods and seeds.

**RQ2.** Does horizon-specific adaptation with causal volatility scaling reduce persistent miscoverage at a useful width compared with static, rolling and established adaptive methods?

**H2.** The candidate improves regime-specific coverage and interval score following volatility changes; the hypothesis fails if gains depend on excessive width, post hoc grouping or final-period tuning.

These hypotheses are provisional. No new architecture, universal conditional-coverage theorem or completed prospective evidence is claimed.

## 4. Preliminary preparation

The archived original notebook uses 180-day windows, positional encoding, two multi-head attention blocks, Conv1D projections, pooling and a dense output. Saved data evidence is 4,397 raw daily rows through 30 September 2026 and 4,368 feature-complete rows. RobustScaler is fitted on training.

Thirty held-out rolling one-step predictions report MAPE 3.40%, MAE USD 2,702.68 and RMSE USD 3,138.98. Each uses actual preceding observations. Callbacks monitor training loss without a separate validation segment. The separate recursive future path replaces Low while holding other predictors fixed; the 3.40% does not score it. A training-prediction diagnostic is in-sample.

These results demonstrate preparation and identify limitations. They are not a new common benchmark. Exact original snapshot bytes and full exported predictions are unavailable. The foundation code adds independently auditable temporal rules, not a certification of the saved neural metric.

## 5. Research design

Acquire and validate a new daily OHLCV snapshot with retrieval UTC time, package version, source settings, SHA-256 and calendar checks. Original bytes will not be reconstructed from plots or summary metrics. The manifest now records actual acquisition on 8 October 2026: 4,404 dates through 7 October, with byte hash and retrieval metadata. Raw files remain local.

Training, validation, calibration and retrospective dates are specified in the [protocol](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/docs/protocol.md). All relevant labels must be observable and remain within stage boundaries. Historical data have been inspected; that evaluation is retrospective. A future window is eligible only after the required design, snapshot and A–D freezes precede its start. Otherwise a dated amendment must select a new future window.

Start with persistence and trailing geometric drift. Use fixed training-only MASE scaling, MAE, RMSE and relative MAE versus persistence. MAPE is secondary; returns near zero will not be scored by MAPE. Neural comparisons require a frozen feature/training specification and exports recording origin, horizon, information cutoff, fully realised training-label cutoff, selection cutoff and protocol hash.

Direct and recursive forecasts will be matched at each horizon; rolling one-step remains a separate task. Exact attention features/settings will be specified before this comparison in an amendment. Feature, window and strategy ablations will isolate modelling choices; seed variation and fit cost will be recorded.

Interval evaluation begins with static, rolling and ACI at 80% and 95%, using absolute or causal volatility-normalised scores. Scores from t enter the h-specific pool only at t+h. ACI feedback uses the threshold issued for that forecast. Rank selection and unbounded finite-sample cases are explicit. EnbPI and other established methods will be implemented and audited before claiming a comparison with them.

Volatility groups use trailing thirty-day Low-log changes and training-fitted terciles. Report sample counts, coverage, width and interval score by horizon, group and time block. Groups with fewer than one hundred observations are inconclusive. The candidate will be ablated by removing normalisation, horizon separation and adaptive updates. Synthetic shifts help isolate mechanisms; they are not financial evidence.

The primary family compares normalised ACI with normalised rolling interval score across four horizons and two levels, with Holm adjustment. Dependence-aware uncertainty and block-length sensitivity will be reported. DM and Kupiec/Christoffersen are assumption-sensitive diagnostics, with minimum evidence requirements; overlapping horizons do not supply independent samples. Profitability is outside the initial scope.

## 6. Contributions and feasibility

The intended empirical contribution is a reproducible account of which horizon strategies survive matched baselines and changing volatility. The methodological contribution is either a tested targeted adaptation or evidence explaining why simpler established methods suffice. The reproducibility contribution is an auditable chain from acquisition to frozen choices, per-origin outputs and reviewed tables.

The initial implementation uses lightweight offline baselines and interval foundations. Neural fitting and broader competitors follow after data and temporal checks. Main risks are revisions, target/calendar conventions, sparse volatile groups, unstable neural fits and premature prospective claims. Reduce the comparison family, report inconclusive results and amend future dates rather than backdating.

## 7. Milestones and current status

**Foundation.** BTC scope, preserved original notebook, temporal checks, protocol and synthetic CI. This is the present repository change.

**Data and model freeze.** Acquire the snapshot, reconcile conventions and lock the exact attention feature/training specification. These steps remain pending.

**Retrospective A–D.** Baselines, horizon strategies, calibration competitors and ablations with complete run records. No BTC run under this protocol is published.

**Prospective evaluation.** Freeze the earlier stages before a genuinely future window. The candidate dates and late-completion rule are in the registration record. No prospective predictions or outcomes are claimed.

**Doctoral extension.** Refine novelty with the supervisor, replicate on additional BTC periods and complete the thesis. Extra instruments are optional subsequent studies, not part of the initial claim.

## 8. Reproducibility and claims

[Registration status](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/docs/preregistration.md) distinguishes a foundation design tag from a complete study preregistration. Missing acquisition evidence is explicit in the [data card](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/docs/data_card.md). The 3.40% saved score belongs to the archived notebook; new code has no new BTC accuracy evidence.

docs/proposal.md is the single active proposal source. Word is generated on demand and checked before sharing. VN30, BID and earlier supplementary results remain in legacy/ as historical preparation; they are not pooled into BTC findings.

## References

[1] Hyndman, R. J., and Athanasopoulos, G. (2021). [Forecasting: Principles and Practice, 3rd edition](https://otexts.com/fpp3/). OTexts.

[2] Hyndman, R. J., and Koehler, A. B. (2006). [Another look at measures of forecast accuracy](https://doi.org/10.1016/j.ijforecast.2006.03.001). International Journal of Forecasting, 22(4), 679–688.

[3] Tashman, L. J. (2000). [Out-of-sample tests of forecasting accuracy: an analysis and review](https://www.sciencedirect.com/science/article/pii/S0169207000000650). International Journal of Forecasting, 16(4), 437–450.

[4] Hewamalage, H., Ackermann, K., and Bergmeir, C. (2023). [Forecast evaluation for data scientists: common pitfalls and best practices](https://arxiv.org/abs/2203.10716). Data Mining and Knowledge Discovery. Author preprint.

[5] Diebold, F. X., and Mariano, R. S. (1995). [Comparing Predictive Accuracy](https://doi.org/10.1080/07350015.1995.10524599). Journal of Business & Economic Statistics, 13(3), 253–263.

[6] Harvey, D., Leybourne, S., and Newbold, P. (1997). [Testing the equality of prediction mean squared errors](https://www.sciencedirect.com/science/article/abs/pii/S0169207096007194). International Journal of Forecasting, 13(2), 281–291.

[7] Holm, S. (1979). [A Simple Sequentially Rejective Multiple Test Procedure](https://www.jstor.org/stable/4615733). Scandinavian Journal of Statistics, 6(2), 65–70.

[8] Politis, D. N., and Romano, J. P. (1994). [The Stationary Bootstrap](https://doi.org/10.1080/01621459.1994.10476870). Journal of the American Statistical Association, 89(428), 1303–1313.

[9] Hansen, P. R., Lunde, A., and Nason, J. M. (2011). [The Model Confidence Set](https://doi.org/10.3982/ECTA5771). Econometrica, 79(2), 453–497.

[10] Meese, R. A., and Rogoff, K. (1983). [Empirical exchange rate models of the seventies: Do they fit out of sample?](https://www.sciencedirect.com/science/article/pii/002219968390017X). Journal of International Economics, 14(1–2), 3–24.

[11] Welch, I., and Goyal, A. (2008). [A Comprehensive Look at The Empirical Performance of Equity Premium Prediction](https://doi.org/10.1093/rfs/hhm014). The Review of Financial Studies, 21(4), 1455–1508.

[12] Triebe, O., Hewamalage, H., Pilyugina, P., Laptev, N., Bergmeir, C., and Rajagopal, R. (2021). [NeuralProphet: Explainable Forecasting at Scale](https://arxiv.org/abs/2111.15397). arXiv:2111.15397.

[13] Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł., and Polosukhin, I. (2017). [Attention Is All You Need](https://arxiv.org/abs/1706.03762). Advances in Neural Information Processing Systems, 30.

[14] Geurts, P., Ernst, D., and Wehenkel, L. (2006). [Extremely randomized trees](https://doi.org/10.1007/s10994-006-6226-1). Machine Learning, 63, 3–42.

[15] Gneiting, T., and Raftery, A. E. (2007). [Strictly Proper Scoring Rules, Prediction, and Estimation](https://doi.org/10.1198/016214506000001437). Journal of the American Statistical Association, 102(477), 359–378.

[16] Romano, Y., Patterson, E., and Candès, E. J. (2019). [Conformalized Quantile Regression](https://arxiv.org/abs/1905.03222). Advances in Neural Information Processing Systems, 32.

[17] Angelopoulos, A. N., and Bates, S. (2021). [A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification](https://arxiv.org/abs/2107.07511). arXiv:2107.07511.

[18] Barber, R. F., Candès, E. J., Ramdas, A., and Tibshirani, R. J. (2021). [The limits of distribution-free conditional predictive inference](https://arxiv.org/abs/1903.04684). Information and Inference, 10(2), 455–482.

[19] Barber, R. F., Candès, E. J., Ramdas, A., and Tibshirani, R. J. (2023). [Conformal prediction beyond exchangeability](https://arxiv.org/abs/2202.13415). The Annals of Statistics, 51(2), 816–845.

[20] Gibbs, I., and Candès, E. (2021). [Adaptive Conformal Inference Under Distribution Shift](https://arxiv.org/abs/2106.00170). Advances in Neural Information Processing Systems, 34.

[21] Gibbs, I., and Candès, E. J. (2024). [Conformal Inference for Online Prediction with Arbitrary Distribution Shifts](https://jmlr.org/papers/v25/22-1218.html). Journal of Machine Learning Research, 25(162), 1–36.

[22] Xu, C., and Xie, Y. (2021). [Conformal prediction interval for dynamic time-series](https://proceedings.mlr.press/v139/xu21h.html). Proceedings of the 38th International Conference on Machine Learning, PMLR 139, 11559–11569.

[23] Zaffran, M., Feron, O., Goude, Y., Josse, J., and Dieuleveut, A. (2022). [Adaptive Conformal Predictions for Time Series](https://proceedings.mlr.press/v162/zaffran22a.html). Proceedings of the 39th International Conference on Machine Learning, PMLR 162, 25834–25866.

## Amendment and evidence boundary

[Amendment 001](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/docs/amendments/amendment-001.md) preserves protocol-v1. Preparation bridge: 2026-10-01–2027-01-31. Candidate future window: 2027-02-01–2027-07-30, conditional on full A–D freeze before its start. [Audit](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/docs/audit-2026-10-08.md). Stage A covers simple baselines; B–D, superiority and prospective evidence remain pending.

## Stage A baseline evidence (8 October 2026)

The real BTC run scores 1,003/999/984/974 origins at h=1/5/20/30. Persistence MAE is USD 1,309.84/3,225.03/6,497.42/8,176.55; drift relative MAE is 1.0005/1.0137/1.0686/1.1017. Drift therefore does not improve descriptive MAE in this period. These are not significance tests and do not compare the archived attention run on different dates. [Tables and provenance](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/results/tables/README.md).
