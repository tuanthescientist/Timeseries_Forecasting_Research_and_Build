# BTC Forecasting and Interval Calibration Under Delayed Feedback

Proposed doctoral research · Trần Anh Tuân · 8 October 2026

## Abstract

Prediction errors arrive late. For a thirty-day forecast, an adaptive calibrator must wait thirty days before learning whether its interval covered the outcome. I investigate how this delay interacts with volatility changes in BTC-USD daily-Low forecasting. The study compares horizon-specific calibration methods using identical point forecasts, separating the effects of volatility scaling, recent residual information and adaptive updates. Attention models are evaluated against persistence and drift; interval comparators include static and rolling calibration, ACI, EnbPI and a target-matched GARCH model. A locked daily snapshot and completed baseline stage provide the empirical starting point. Evaluation combines interval score, coverage by volatility group, mean width and persistent undercoverage, with explicit rules for inconclusive cases. The expected contribution is an empirical account of when delayed adaptation offers a useful coverage–width trade-off and when it fails. A separately frozen future window will assess the completed design. The study will test the proposed combination against explicit decision margins.

## 1. Introduction

The original notebook gave me a concrete starting point: 3.40% MAPE over thirty rolling one-step predictions. Reading that number alongside the forecast construction reveals a distinction that matters for this proposal. Each one-step prediction uses newly observed history. I therefore treat the saved result as implementation experience and make horizon alignment a condition of the new comparison. Stage A sharpens that decision. Persistence beats geometric drift in descriptive MAE at all four horizons, even though drift is a plausible extrapolation of recent price growth. I retain that result because it sets a useful standard for the attention model: complexity has to improve the same task, on the same origins, before its apparent accuracy becomes persuasive.

Feedback takes time. At origin t, a one-day error becomes observable at t+1, whereas a thirty-day error arrives at t+30, 29 days later than the one-day error. The experiment asks whether a calibrator can respond to a volatility transition while much of its recent forecast history is still unresolved. Sustained undercoverage is the hypothesis this interval evaluation will test.

I focus on BTC Low because it connects directly to the original implementation and gives the comparison a single target. It is the vendor-reported minimum of a UTC daily bar, not an executable trading price. I keep VN30 and BID as earlier work rather than pooling their different targets, calendars and saved evaluation designs into this claim. Close and intraday realised variance could support later target comparisons.

The [timeline](#8-timeline) sets out the four retrospective stages and the subsequent future evaluation.

## 2. Background

Chronological evaluation, matching horizons and suitable losses [1–4] motivate persistence and drift benchmarks. I take the benchmark discipline from financial forecasting evidence [10, 11], rather than treating its exchange-rate and equity-premium findings as a prediction about BTC Low. Attention [13] is a modelling component whose value must be measured under equal information access. NeuralProphet [12] and ExtraTrees [14] represent earlier implementation experience.

Proper interval scoring [15], conformalized quantile regression [16] and conformal foundations [17] provide uncertainty-evaluation tools. Conditional-inference limits [18] and methods beyond exchangeability [19] clarify the need for empirical financial-data checks. ACI [20, 21], EnbPI [22] and adaptive aggregation [23] are established competitors. I use interval score to assess width and misses together, and retain group coverage to expose failures hidden by an overall average. Neither measure alone answers the research question. The proposed method combines horizon-specific scores, volatility scaling and delayed ACI updates; establishing whether that combination adds anything beyond existing methods is part of the work.

ARCH [26] and GARCH [27] motivate an explicit conditional-variance comparator. Patton [28] explains how imperfect volatility proxies can affect forecast rankings. Trailing dispersion of Low-log changes is an observable proxy, not validated latent integrated volatility. GARCH supplies a financial comparator for this proxy-based task. Intraday realised-volatility methods [29] require measurements beyond daily OHLCV.

The research gap to investigate is the interaction of horizon-dependent feedback delay and volatility transitions under matched forecasts and information sets. Predictive-accuracy tests [5, 6], multiplicity adjustment [7] and dependent-data resampling [8] inform inference; model confidence sets [9] are optional. Kupiec [24] and Christoffersen [25] provide coverage diagnostics whose assumptions need particular care for overlapping horizons.

Table 1 distinguishes the role of each comparator and the setting in which its coverage statements apply.

**Table 1. Comparators, updating mechanisms and coverage assumptions.**

| Method | Updating mechanism | Assumptions and guarantee scope | Question in this study |
| --- | --- | --- | --- |
| Static split conformal [17] | Fixed calibration scores | Standard finite-sample marginal coverage uses exchangeable calibration/test scores | How much does a fixed pool deteriorate after a volatility change? |
| Rolling calibration | Recent realised scores replace older scores | A rolling window alone gives no arbitrary-dependence coverage guarantee | Does recent information suffice without adapting the error level? |
| ACI [20, 21] | Error feedback adjusts the effective miscoverage level | Long-run frequency control in the specified online setting; not a universal local or conditional guarantee | What changes when feedback arrives h days after issue? |
| EnbPI [22] | Bootstrap ensemble and sequential residual updates | Approximate marginal coverage under stated regression/error conditions, including strongly mixing errors | Can an established ensemble comparator improve the same task with delayed feedback? |
| GARCH [26, 27] | Conditional variance filtering and periodic parameter refits | Parametric variance/innovation specification; interval calibration depends on model adequacy | How does a financial volatility model compare on the same Low target? |

## 3. Research questions and hypotheses

**RQ1.** Which attention strategy improves point accuracy over persistence at a fixed forecast horizon?

**H1.** An attention strategy selected on chronological validation achieves lower mean absolute error than persistence on matched evaluation origins. Support is assessed separately at each horizon, rather than inferred from a pooled score.

Direct and recursive forecasts are compared at the same horizon. Rolling one-step is evaluated only at h=1. Window and feature selection occur before the evaluation period; their search space and seed aggregation will be fixed before Stage B. This distinguishes a forecast-strategy effect from access to newer observations.

**RQ2.** Does volatility-scaled delayed ACI improve interval calibration over volatility-scaled rolling calibration using identical point forecasts?

**H2.** Volatility-scaled delayed ACI lowers mean interval score and persistent undercoverage while meeting the specified group-coverage tolerance and increasing mean width by no more than 10% relative to rolling calibration.

This hypothesis retains the practical width allowance rather than requiring equal width. It asks whether adaptation provides a measurable benefit at a bounded cost. The definitions and joint decision rule appear in Table 2. Each horizon and coverage level receives its own assessment.

I distinguish failure from insufficient evidence. A method can fail a width or accuracy condition, while too few realised blocks can leave the adaptation claim unresolved. Both outcomes are relevant to the usefulness of a delayed calibrator.

## 4. Method overview

The proposed method combines three components: horizon-specific scores, volatility scaling and delayed ACI. Whether this combination improves on existing methods is the central empirical question. [Appendix A](#appendix-a-method-specification) gives the equations and boundary conventions.

First, each model and horizon maintains its own residual history. A forecast enters that history only when its outcome is observable. At h=30, a forecast issued today therefore cannot affect calibration tomorrow. Keeping the issue and realisation times explicit makes the information available to each comparator comparable.

Second, the volatility-scaled score divides the absolute forecast error by a scale fixed at the forecast origin. That scale combines Low, trailing thirty-day dispersion of Low-log changes and the square root of the horizon. I treat this scaling as an approximation to test. Absolute-residual variants isolate whether it helps beyond using a recent calibration pool.

Third, delayed ACI updates its effective miscoverage level when an issued interval can be scored. Rolling calibration uses the same available scores with a fixed level. Comparing the two on identical point forecasts isolates the contribution of adaptation, while static calibration shows the effect of retaining an unchanged pool.

The financial comparator is a constant-mean GARCH(1,1) with standardised Student-t innovations fitted to Low-log changes. Simulated cumulative changes are transformed back into Low-price intervals at each horizon. This gives a target-matched comparison with explicit variance dynamics. EnbPI provides a separate established conformal comparator.

Synthetic volatility shifts will isolate these mechanisms before the BTC evaluation. Ablations compare absolute and volatility-scaled scores, and fixed and adaptive levels. Pooling different horizons is only a labelled stress test. It cannot substitute for the primary horizon-specific comparison.

## 5. Evaluation and decision rules

Training: 2014-09-17–2021-12-31; validation: 2022-01-01–2023-06-30; calibration: 2023-07-01–2023-12-31; retrospective evaluation: 2024-01-01–2026-09-30. Fitting labels must be observed and scored endpoints stay within their stage. The unscored preparation bridge is 2026-10-01–2027-01-31. The conditional future window is 2027-02-01–2027-07-30 under [Amendment 001](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/docs/amendments/amendment-001.md). Historical data and Stage A have already been inspected.

The comparison retains persistence and 252-day geometric drift as the point baselines. Direct and recursive attention are compared at matching horizons, with rolling one-step evaluated at h=1. The specified windows are 90 and 180 days; seeds are 42, 123 and 2026, with refits every 30 days. Selection uses validation mean relative MAE.

The full attention specification must fix causal features, architecture, early stopping, realised training-label access and seed aggregation before Stage B. Point metrics are MAE, RMSE, fixed-training MASE, relative MAE and secondary price MAPE.

Each forecast record will contain:

- Forecast origin and horizon.
- Information cutoff.
- Training-label cutoff.
- Selection cutoff.
- Protocol hash.

These proposed decision margins will be frozen in a full-study amendment before Stage B, following validation/synthetic feasibility assessment.

**Table 2. Draft H2 decision criteria for each horizon and coverage level.**

| Criterion | Draft operational definition |
| --- | --- |
| Interval accuracy | Negative mean interval-score difference, supported by dependence-aware testing and Holm adjustment; see [Appendix B](#appendix-b-statistical-details) |
| Group calibration | Absolute coverage deviation from nominal at most 5 percentage points in every volatility group with at least 100 paired outcomes |
| Useful width | Mean ACI width / mean rolling width at most 1.10, overall and within each eligible group |
| Persistent undercoverage | Coverage below nominal minus 5 percentage points in two adjacent non-overlapping 60-origin blocks |
| Adaptation benefit | Fewer adjacent block pairs exhibiting persistent undercoverage than rolling; if rolling has none, this benefit is inconclusive |

For H1, improvement requires relative MAE below 1 and a dependence-aware confidence interval for the paired mean absolute-loss difference excluding zero in the favourable direction. The neural comparison family and seed aggregation must be fixed before testing.

For H2, all Table 2 criteria must hold for a horizon/level to receive support. A claim across all four horizons and two levels requires all eight assessments to pass. [Appendix B](#appendix-b-statistical-details) specifies block construction, uncertainty, multiplicity and inconclusive cases.

Public aggregate metrics and run provenance support inspection of the reported results. Independent recomputation requires the exact raw snapshot, which remains local with the full predictions. Vendor revisions may prevent exact restoration; the [data card](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/docs/data_card.md) explains access and provenance.

## 6. Preliminary evidence

The archived TensorFlow notebook uses 180-day windows, positional encoding, two multi-head attention blocks, Conv1D projections, pooling and a dense output. RobustScaler is fitted on training. Thirty rolling one-step predictions report MAPE 3.40%, MAE USD 2,702.68 and RMSE USD 3,138.98. Callbacks monitor training loss without a separate validation segment. A separate recursive path holds other features fixed and is not scored by that MAPE. Original snapshot bytes are unavailable.

The new snapshot has 4,404 daily observations from 2014-09-17 through 2026-10-07, acquired on 8 October 2026. Stage A scores origins in 2024-01-01–2026-09-30 whose endpoints remain inside that period:

| Horizon | Origins | Persistence MAE (USD) | Drift / persistence MAE |
| --- | ---: | ---: | ---: |
| 1 | 1,003 | 1,309.84 | 1.0005 |
| 5 | 999 | 3,225.03 | 1.0137 |
| 20 | 984 | 6,497.42 | 1.0686 |
| 30 | 974 | 8,176.55 | 1.1017 |

Drift does not improve descriptive MAE. This motivates a demanding baseline for attention, but is not a significance result or a matched comparison with the archived thirty-day experiment. [Tables and provenance](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/results/tables/README.md).

## 7. Contribution and risks

**The expected contribution is a controlled empirical account of how horizon-dependent feedback delay and volatility scaling jointly determine calibration, sharpness and persistent interval failures for BTC daily-Low forecasts.**

The experiment separates point-model, scaling and adaptation effects and identifies their failure conditions. Any later algorithmic innovation must be justified by these findings and compared with established adaptive methods. Negative results remain useful when they explain failed assumptions or unchanged benchmark rankings.

Risks include sparse regimes, dependent outcomes, noisy volatility proxies, unstable neural/GARCH fits and an incomplete future-window freeze. Prioritise matched baselines and the eight-comparison interval family. Optional comparators can be deferred before the final freeze. Changes to core requirements require a documented design amendment. If the attention specification is incomplete by 31 October, I will postpone Stage B until it is frozen and revise downstream dates, including the future window through an amendment if needed.

Stage A is complete; neural, interval and future evaluations are the remaining work. The future evaluation will test whether any observed benefit persists after the full-study freeze.

## 8. Timeline

| Milestone | Planned dates | Deliverable |
| --- | --- | --- |
| 1. Foundation and Stage A | Completed 8 October 2026 | Locked snapshot, baseline table and provenance |
| 2. Full specification | 9–31 October 2026, conditional target | Attention features/training, H2 margins, GARCH and inference details; feasibility review on 16 October; dated amendment |
| 3. Stage B | November 2026 | Matched attention forecasts, seeds, selection records and cost |
| 4. Stages C–D | December 2026–15 January 2027 | Stage C: interval and GARCH comparisons with group diagnostics. Stage D: ablations and sensitivity. |
| 5. Review and freeze | 16–31 January 2027 | Complete A–D review and published full-study lock before 1 February UTC |
| 6. Conditional future evaluation | 1 February–30 July 2027 | Frozen forecast/update rules; endpoint analysis after all outcomes close |
| 7. Interpretation and doctoral development | August–September 2027 | Final comparisons, limitations and supervisor-led extension |

### Compute budget and feasibility

A full-grid planning scenario has 34 fit rounds, including the initial fit, over approximately 1,000 origins with refits every 30 days. Two windows × three seeds × six fits per round gives **34 × 2 × 3 × (4 direct + 1 recursive + 1 rolling) = 1,224 neural fits**. This assumes separate direct models for four horizons and independent recursive/rolling fits. If their training specifications are identical, reusing the same one-step model reduces the count to 1,020. Such reuse requires an explicit specification.

The following are illustrative timing scenarios, not measured runtimes. They assume a constant mean fit duration and serial execution on one training device.

| Assumed mean time per fit | Training time for 1,224 fits | Continuous device-days |
| --- | ---: | ---: |
| 5 minutes | 102 hours | 4.25 |
| 15 minutes | 306 hours | 12.75 |
| 30 minutes | 612 hours | 25.50 |

This full-grid scenario budgets both windows; validation-based selection may reduce the final evaluation grid. It excludes validation searches, warm calibration fits, feature ablations, failed-run retries, inference, GARCH and future-period refits. Their costs must be added before allocating resources. Parallel execution depends on device availability and memory, so no speed-up is assumed.

A validation-only timing pilot will record hardware, sample size, window, batch size, epochs, stopping rule, wall time and peak memory. The resulting measurements will replace these scenarios at the 16 October review. If the budget exceeds available compute or the deadline, optional experiments will be deferred before the full-study freeze, or the schedule will move through an amendment.

The attention specification is the immediate bottleneck. Features, training-label availability and seed aggregation still need to be settled. On 16 October, I will review the specification checklist, available compute and a validation-only estimate of training cost and seed variability. That review will determine whether the 31 October target is feasible.

If the review exposes unresolved dependencies, I will revise the work plan immediately. Any resulting change to the study design or future window requires a dated amendment. The January review remains the final checkpoint for a complete freeze before February.

Historical observations have already been inspected, so their analysis is retrospective. The future evaluation requires the complete study to be frozen before its window begins.

## Appendix A. Method specification

### A.1 Information, scale and groups

Let $Y_t>0$ denote Low and $\mathcal F_t$ the observations available after day t closes. Forecast $\widehat Y_{t,h}$ uses only $\mathcal F_t$, for $h\in\{1,5,20,30\}$. Define

$$
r_t=\log(Y_t/Y_{t-1}),\quad
\bar r_t=\frac1{30}\sum_{i=t-29}^{t}r_i,\quad
v_t=\left[\frac1{30}\sum_{i=t-29}^{t}(r_i-\bar r_t)^2\right]^{1/2},
\quad b_{t,h}=\max(10^{-8},Y_t v_t\sqrt h).
$$

I use square-root-h scaling as a testable approximation; the ablation will show whether it helps at longer horizons. Training-only terciles $c_1,c_2$ are fitted once to eligible training $v_t$ values, using linear interpolation at sorted positions $(n-1)/3$ and $2(n-1)/3$. Groups are low if $v_t\le c_1$, medium if $c_1<v_t\le c_2$, and high otherwise. Every method uses the same fixed grouping.

### A.2 Scores, pools, intervals and updates

For each model and horizon separately, define

$$
s_{j,h}=\frac{|Y_{j+h}-\widehat Y_{j,h}|}{b_{j,h}},\qquad
\mathcal P_{t,h}=\operatorname{last}_{500}
\{s_{j,h}:j+h\le t,\ j\text{ is an eligible calibration or earlier evaluation origin}\}.
$$

Scores retain their origin-time scale and enter in realisation order. Warm calibration labels must mature before evaluation starts. Static calibration keeps its fixed warm pool; rolling and ACI use up to 500 recent available scores. Absolute-residual variants set b=1. Models and horizons do not share pools.

For $n=|\mathcal P_{t,h}|$, nominal miscoverage $\alpha\in\{0.20,0.05\}$, and adaptive state $a_{t,h,\alpha}$,

$$
k=\left\lceil(n+1)(1-a_{t,h,\alpha})\right\rceil,\quad
q_{t,h,\alpha}=s_{(k)},\quad
I_{t,h,\alpha}=
[\widehat Y_{t,h}-b_{t,h}q_{t,h,\alpha},
 \widehat Y_{t,h}+b_{t,h}q_{t,h,\alpha}].
$$

An empty pool cannot issue an interval. If $1-a\le0$, q=0; if $1-a\ge1$ or k>n, q is infinite; otherwise use the k-th ascending score. These conventions match the foundation implementation. Report infinite width and score explicitly; do not drop unbounded intervals or clip negative lower bounds.

Static/rolling methods fix a=alpha. ACI starts at a=alpha and, when an issued forecast from j matures, updates its model/horizon/level state once:

$$
a\leftarrow a+\gamma\left(\alpha-
\mathbf1\{Y_{j+h}\notin I_{j,h,\alpha}^{\mathrm{issued}}\}\right),
\qquad\gamma=0.005.
$$

Process matured feedback before issuing the next interval. Use the historical issued threshold, not a recomputed one. The foundation does not clip a. This delayed variant is evaluated empirically; a guarantee for another feedback setting is not automatically inherited.

### A.3 GARCH comparator

Fit a constant-mean GARCH(1,1) to the same Low-log changes with standardised Student-t innovations [26, 27]:

$$
r_t=\mu+\epsilon_t,\qquad \epsilon_t=\sigma_t z_t,\qquad
\sigma_t^2=\omega+\beta_1\epsilon_{t-1}^2+\beta_2\sigma_{t-1}^2.
$$

Require $\omega>0,\ \beta_1,\beta_2\ge0,\ \beta_1+\beta_2<1$, unit innovation variance and degrees of freedom above 2. Draft settings are an expanding causal fit, a 30-day refit schedule, daily filtering and 10,000 simulated paths per origin with a fixed recorded seed. Transform each path into $Y_t\exp(\sum_{k=1}^{h}r_{t+k})$, then take alpha/2 and 1−alpha/2 quantiles. This comparator is designed to fit the Low-log-change process; its adequacy for multi-step intervals will be evaluated empirically. Log convergence failures and paired-sample counts rather than silently dropping failed origins or substituting another model. Solver, initialisation, seed, quantile convention and failure policy must be frozen before implementation. This comparator is proposed, not executed or included in the existing lock.

## Appendix B. Statistical details

### B.1 Metrics

For an interval [L,U] and outcome y, use the central interval score [15]:

$$
IS_\alpha(L,U;y)=(U-L)
+\frac{2}{\alpha}(L-y)\mathbf1\{y<L\}
+\frac{2}{\alpha}(y-U)\mathbf1\{y>U\}.
$$

Lower is better. Alpha is total two-sided miscoverage and the penalty is $2/\alpha$. On common realised origins G, report coverage
$\widehat C_G=|G|^{-1}\sum_{t\in G}\mathbf1\{Y_{t+h}\in I_{t,h,\alpha}\}$,
mean width $\bar W_G=|G|^{-1}\sum_{t\in G}(U-L)$, and mean interval score.

### B.2 Blocks and joint decisions

**Block construction.** Blocks begin at the first common eligible origin. Score each block after all endpoints mature. Exclude and count incomplete blocks. Overlapping outcomes still make block summaries dependent.

**Inconclusive cases.** Undefined width ratios, insufficient group counts or too few blocks yield insufficient evidence. An infinite width for the proposed method instead fails the finite-width criterion.

**Joint support.** Every criterion must hold for a horizon/level to receive support. A benefit across all horizons/levels requires all eight assessments to pass. Report each component even when the joint criterion fails.

**Decision margins.** The 5-point coverage tolerance and 10% width allowance are proposed design choices. Assess precision on validation and synthetic shifts, then freeze the margins before Stage B.

**Sensitivity analysis.** Use coverage tolerances of 2/10 percentage points, width ratios of 1.05/1.20 and block lengths of 30/90 as descriptive alternatives. These results cannot replace a failed primary criterion.

**Future-window limits.** The 180-day window may contain too few group observations or complete blocks, especially at h=30. Report insufficient evidence rather than relaxing criteria after observing outcomes.

### B.3 Dependent losses and multiplicity

**Primary family.** Compare volatility-scaled delayed ACI with volatility-scaled rolling interval score across four horizons and two levels. Holm adjustment targets familywise error at 5%, subject to valid component tests.

**Resampling.** Circular block bootstrap uses 30-day blocks. Repeat with 15-day and 60-day blocks to assess sensitivity to the dependence approximation.

**Predictive-accuracy diagnostic.** The Bartlett-HAC DM diagnostic follows Amendment 001. Its minimum sample size is max(50,5h).

**Undefined comparisons.** Freeze the test construction and treatment of infinite scores before inference. A comparison with undefined finite means is inconclusive.

**Coverage diagnostics.** Kupiec [24] assesses miss frequency; Christoffersen [25] examines dependence in the hit sequence. Treat both as secondary diagnostics. Overlapping horizons prevent an independent-Bernoulli interpretation. Report non-overlapping-origin sensitivity alongside its reduced sample size.

Trading profitability is outside scope.

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

[24] Kupiec, P. H. (1995). [Techniques for Verifying the Accuracy of Risk Measurement Models](https://doi.org/10.3905/jod.1995.407942). The Journal of Derivatives, 3(2), 73–84.

[25] Christoffersen, P. F. (1998). [Evaluating Interval Forecasts](https://doi.org/10.2307/2527341). International Economic Review, 39(4), 841–862.

[26] Engle, R. F. (1982). [Autoregressive Conditional Heteroscedasticity with Estimates of the Variance of United Kingdom Inflation](https://doi.org/10.2307/1912773). Econometrica, 50(4), 987–1007.

[27] Bollerslev, T. (1986). [Generalized autoregressive conditional heteroskedasticity](https://doi.org/10.1016/0304-4076(86)90063-1). Journal of Econometrics, 31(3), 307–327.

[28] Patton, A. J. (2011). [Volatility forecast comparison using imperfect volatility proxies](https://doi.org/10.1016/j.jeconom.2010.03.034). Journal of Econometrics, 160(1), 246–256.

[29] Andersen, T. G., Bollerslev, T., Diebold, F. X., and Labys, P. (2003). [Modeling and Forecasting Realized Volatility](https://doi.org/10.1111/1468-0262.00418). Econometrica, 71(2), 579–625.
