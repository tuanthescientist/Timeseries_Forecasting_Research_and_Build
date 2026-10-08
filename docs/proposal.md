# BTC Forecasting and Interval Calibration Under Delayed Feedback

Proposed doctoral research · Trần Anh Tuấn · 8 October 2026

## Abstract

This project investigates how forecast horizon and delayed error feedback affect prediction-interval calibration for BTC-USD daily Low during volatility changes. It compares attention forecasts with simple point baselines, and static, rolling and adaptive calibration with a financial volatility comparator. The central experiment holds forecasts and information sets fixed while varying residual scaling and adaptive updates at horizons of 1, 5, 20 and 30 days. The expected contribution is an empirical characterization of when delayed, volatility-normalised adaptation improves coverage and sharpness, and when it fails. A locked snapshot and completed Stage A provide initial evidence: geometric drift has higher MAE than persistence at all four horizons. The remaining stages test the interval mechanism and evaluate a fully frozen design on future observations.

## 1. Motivation and scope

At forecast origin t, an h-day error becomes available only at t+h. Longer horizons therefore slow the feedback available to a calibrator during volatility changes. Average coverage can conceal sustained failures within volatile periods. The research problem is to measure this interaction while separating point-forecast quality from interval behaviour.

The target is Yahoo Finance BTC-USD daily Low after each UTC day closes. It is a reported daily-bar minimum, not an executable trading price. Low-to-Low log changes provide a target-aligned variability proxy. Forecasting Close or intraday realised variance requires a separate target and measurement design.

## 2. Related work and research gap

Chronological evaluation, matching horizons and suitable losses [1–4] motivate persistence and drift benchmarks. Financial forecasting evidence [10, 11] reinforces their importance without determining the outcome for BTC Low. Attention [13] is a modelling component whose value must be measured under equal information access. NeuralProphet [12] and ExtraTrees [14] represent earlier implementation experience.

Proper interval scoring [15], conformalized quantile regression [16] and conformal foundations [17] provide uncertainty-evaluation tools. Conditional-inference limits [18] and methods beyond exchangeability [19] clarify the need for empirical financial-data checks. ACI [20, 21], EnbPI [22] and adaptive aggregation [23] are established competitors. Combining horizon-specific scores, volatility scaling and delayed ACI updates defines the operational candidate here; the combination alone does not establish methodological novelty.

ARCH [26] and GARCH [27] motivate an explicit conditional-variance comparator. Patton [28] explains how imperfect volatility proxies can affect forecast rankings. Trailing dispersion of Low-log changes is an observable proxy, not validated latent integrated volatility. Intraday realised-volatility methods [29] inform a later extension; daily OHLCV cannot reproduce their measurement design.

The research gap to investigate is the interaction of horizon-dependent feedback delay and volatility transitions under matched forecasts and information sets. Predictive-accuracy tests [5, 6], multiplicity adjustment [7] and dependent-data resampling [8] inform inference; model confidence sets [9] are optional. Kupiec [24] and Christoffersen [25] provide coverage diagnostics whose assumptions need particular care for overlapping horizons.

## 3. Questions, operational method and hypotheses

**Design status.** The equations specify the existing foundation mechanism. H2 decision margins and the GARCH comparator below are draft additions requiring validation/synthetic feasibility checks and a dated full-study amendment before B–D comparison. They are not settings frozen by protocol-v1.1, and have not been selected using interval results.

### 3.1 Information, scale and groups

Let $Y_t>0$ denote Low and $\mathcal F_t$ the observations available after day t closes. Forecast $\widehat Y_{t,h}$ uses only $\mathcal F_t$, for $h\in\{1,5,20,30\}$. Define

$$
r_t=\log(Y_t/Y_{t-1}),\quad
\bar r_t=\frac1{30}\sum_{i=t-29}^{t}r_i,\quad
v_t=\left[\frac1{30}\sum_{i=t-29}^{t}(r_i-\bar r_t)^2\right]^{1/2},
\quad b_{t,h}=\max(10^{-8},Y_t v_t\sqrt h).
$$

The square-root-h scale is a causal heuristic to test, not an assumed BTC variance law. Training-only terciles $c_1,c_2$ are fitted once to eligible training $v_t$ values, using linear interpolation at sorted positions $(n-1)/3$ and $2(n-1)/3$. Groups are low if $v_t\le c_1$, medium if $c_1<v_t\le c_2$, and high otherwise. Every method uses the same fixed grouping.

### 3.2 Scores, pools, intervals and updates

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

### 3.3 Scoring and testable hypotheses

For an interval [L,U] and outcome y, use the central interval score [15]:

$$
IS_\alpha(L,U;y)=(U-L)
+\frac{2}{\alpha}(L-y)\mathbf1\{y<L\}
+\frac{2}{\alpha}(y-U)\mathbf1\{y>U\}.
$$

Lower is better. Alpha is total two-sided miscoverage and the penalty is $2/\alpha$. On common realised origins G, report coverage
$\widehat C_G=|G|^{-1}\sum_{t\in G}\mathbf1\{Y_{t+h}\in I_{t,h,\alpha}\}$,
mean width $\bar W_G=|G|^{-1}\sum_{t\in G}(U-L)$, and mean interval score.

**RQ1 / H1.** Which attention strategy improves point accuracy at each fixed horizon? Improvement requires relative MAE below 1 against persistence and a dependence-aware confidence interval for the paired mean absolute-loss difference excluding zero favourably. Otherwise improvement is not established. Rolling one-step belongs only to h=1. Freeze the neural comparison family and seed aggregation before Stage B.

**RQ2 / H2.** Does volatility-normalised delayed ACI improve on volatility-normalised rolling intervals with identical point forecasts? Proposed practical criteria are:

| Criterion | Draft operational definition |
| --- | --- |
| Interval accuracy | Negative mean interval-score difference, supported by dependence-aware testing with Holm adjustment over four horizons × two levels |
| Group calibration | Absolute coverage deviation from nominal at most 5 percentage points in every volatility group with at least 100 paired outcomes |
| Useful width | Mean ACI width / mean rolling width at most 1.10, overall and within each eligible group |
| Persistent undercoverage | Coverage below nominal minus 5 percentage points in two adjacent non-overlapping 60-origin blocks |
| Adaptation benefit | Fewer adjacent block pairs exhibiting persistent undercoverage than rolling; if rolling has none, this benefit is inconclusive |

Blocks start at the first common eligible origin and are scored after all endpoints mature. Incomplete blocks are excluded and counted. Overlapping outcomes still make these block summaries dependent. Undefined width ratios, insufficient group counts or too few blocks are inconclusive; infinite candidate width fails the finite-width criterion.

Report support separately for each horizon/level only when all criteria hold. Benefit across all horizons/levels requires all eight to satisfy them. Report every component when the joint criterion fails. The 5-point and 10% margins are proposed design choices, not established literature thresholds; assess precision on validation and synthetic shifts and freeze any changes before interval evaluation. Sensitivity at 2/10 coverage points, width ratios 1.05/1.20 and block lengths 30/90 is descriptive and cannot replace a failed primary criterion. The 180-day future window may lack enough groups or complete blocks, especially at h=30; do not relax criteria after observing outcomes.

## 4. Preliminary evidence

The archived TensorFlow notebook uses 180-day windows, positional encoding, two multi-head attention blocks, Conv1D projections, pooling and a dense output. RobustScaler is fitted on training. Thirty rolling one-step predictions report MAPE 3.40%, MAE USD 2,702.68 and RMSE USD 3,138.98. Callbacks monitor training loss without a separate validation segment. A separate recursive path holds other features fixed and is not scored by that MAPE. Original snapshot bytes are unavailable.

The new snapshot has 4,404 daily observations from 2014-09-17 through 2026-10-07, acquired on 8 October 2026. Stage A scores origins in 2024-01-01–2026-09-30 whose endpoints remain inside that period:

| Horizon | Origins | Persistence MAE (USD) | Drift / persistence MAE |
| --- | ---: | ---: | ---: |
| 1 | 1,003 | 1,309.84 | 1.0005 |
| 5 | 999 | 3,225.03 | 1.0137 |
| 20 | 984 | 6,497.42 | 1.0686 |
| 30 | 974 | 8,176.55 | 1.1017 |

Drift does not improve descriptive MAE. This motivates a demanding baseline for attention, but is not a significance result or a matched comparison with the archived thirty-day experiment. [Tables and provenance](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/results/tables/README.md).

## 5. Experimental design

**Chronology.** Training: 2014-09-17–2021-12-31; validation: 2022-01-01–2023-06-30; calibration: 2023-07-01–2023-12-31; retrospective evaluation: 2024-01-01–2026-09-30. Fitting labels must be observed and scored endpoints stay within their stage. The unscored preparation bridge is 2026-10-01–2027-01-31. The conditional future candidate is 2027-02-01–2027-07-30 under [Amendment 001](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/docs/amendments/amendment-001.md). Historical data and Stage A have already been inspected.

**Point models.** Retain persistence and 252-day geometric drift. Compare direct and recursive attention at matching horizons, with rolling one-step as an h=1 task. The foundation specifies candidate windows 90/180, seeds 42/123/2026, refits every 30 days and validation mean relative MAE for selection. Exact causal features, architecture, early stopping, realised training-label access and seed aggregation need a full-study amendment. Record origin, horizon, information cutoff, training-label cutoff, selection cutoff and protocol hash. Report MAE, RMSE, fixed-training MASE, relative MAE and secondary price MAPE.

**Interval competitors.** Use static, rolling and ACI with absolute and scaled scores. EnbPI [22] needs an implemented, validated adapter. Optional ETS/ARIMA and aggregation [23] follow only if resources permit. Freeze the final family before B–D comparisons.

**Proposed financial comparator.** Fit a constant-mean GARCH(1,1) to the same Low-log changes with standardised Student-t innovations [26, 27]:

$$
r_t=\mu+\epsilon_t,\qquad \epsilon_t=\sigma_t z_t,\qquad
\sigma_t^2=\omega+\beta_1\epsilon_{t-1}^2+\beta_2\sigma_{t-1}^2.
$$

Require $\omega>0,\ \beta_1,\beta_2\ge0,\ \beta_1+\beta_2<1$, unit innovation variance and degrees of freedom above 2. Draft settings are an expanding causal fit, a 30-day refit schedule, daily filtering and 10,000 simulated paths per origin with a fixed recorded seed. Transform each path into $Y_t\exp(\sum_{k=1}^{h}r_{t+k})$, then take alpha/2 and 1−alpha/2 quantiles. This matches the Low target and multi-step variance dynamics. Log convergence failures and paired-sample counts rather than silently dropping failed origins or substituting another model. Solver, initialisation, seed, quantile convention and failure policy must be frozen before implementation. This comparator is proposed, not executed or included in the existing lock.

**Mechanism and inference.** Compare absolute/scaled scores and fixed/adaptive levels on identical point forecasts at each horizon. Pooling unlike horizons is only a labelled stress test. Synthetic volatility shifts isolate feedback mechanisms before financial evaluation.

Retain the primary family of normalised ACI versus normalised rolling interval score, Holm control at familywise 5%, circular block bootstrap with 30-day blocks and sensitivity at 15/60, and the amendment's Bartlett-HAC DM diagnostic with minimum sample size max(50,5h). Freeze the exact test construction and treatment of infinite scores before inference; undefined finite-mean comparisons are inconclusive. Kupiec [24] and Christoffersen [25] are secondary miss-rate/dependence diagnostics. Overlapping horizons prevent interpreting outcomes as independent Bernoulli trials; report non-overlapping-origin sensitivity and its sample-size limitations. Trading profitability is outside scope.

## 6. Expected contribution and feasibility

**The expected contribution is a controlled empirical account of how horizon-dependent feedback delay and volatility scaling jointly determine calibration, sharpness and persistent interval failures for BTC daily-Low forecasts.**

The experiment separates point-model, scaling and adaptation effects and identifies their failure conditions. Any later algorithmic innovation must be justified by these findings and compared with established adaptive methods. Negative results remain useful when they explain failed assumptions or unchanged benchmark rankings.

Risks include sparse regimes, dependent outcomes, noisy volatility proxies, unstable neural/GARCH fits and an incomplete future-window freeze. Prioritise matched baselines and the eight-comparison interval family. Optional comparators can be deferred before the final freeze; core requirements cannot be removed silently to meet a date.

## 7. Dated milestones

| Milestone | Planned dates | Deliverable |
| --- | --- | --- |
| 1. Foundation and Stage A | Completed 8 October 2026 | Locked snapshot, baseline table and provenance |
| 2. Full specification | 9–31 October 2026 | Attention features/training, H2 margins, GARCH and inference details; validation/synthetic feasibility; dated amendment |
| 3. Stage B | November 2026 | Matched attention forecasts, seeds, selection records and cost |
| 4. Stages C–D | December 2026–15 January 2027 | Calibration/GARCH comparisons, ablations, group diagnostics and sensitivity |
| 5. Review and freeze | 16–31 January 2027 | Complete A–D review and published full-study lock before 1 February UTC |
| 6. Conditional future evaluation | 1 February–30 July 2027 | Frozen forecast/update rules; endpoint analysis after all outcomes close |
| 7. Interpretation and doctoral development | August–September 2027 | Final comparisons, limitations and supervisor-led extension |

This is a workload proposal, not a demonstrated four-month completion estimate. Any incomplete full-study requirement at the January review triggers a dated amendment reserving a later future window. Outcomes already observed cannot be relabelled prospective.

## 8. Reproducibility, design status and limitations

The immutable protocol-v1 and active foundation tag protocol-v1.1 are documented in the [registration record](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/docs/preregistration.md). This revision adds explicit exposition and draft design choices without changing the machine-readable lock. B–D, GARCH and prospective evidence remain pending. New-method superiority and universal conditional coverage are not established.

Public Stage A artifacts contain aggregate metrics, source commit, protocol/snapshot hashes and hashes of local per-origin outputs. Raw data and full predictions remain local (raw_predictions_public=false). Independent recomputation needs the exact snapshot; --restore rejects revised vendor bytes. Public tables alone cannot reconstruct the complete evaluation. See the [data card](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/docs/data_card.md).

Historical inspection, the archived attention run's different evaluation dates, imperfect Low-based volatility measurement, dependent multi-step losses and small future group counts constrain conclusions. This Markdown file is the active proposal; Word is an export reviewed when needed. VN30/BID remain historical preparation in legacy/.

New references [24–29] were checked against DOI metadata and primary papers or author/publisher records on 8 October 2026. This does not claim a new full-text audit of references [1–23].

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

[10] Meese, R. A., and Rogoff, K. (1983). [Empirical exchange rate models of the seventies: Do they fit out of sample–](https://www.sciencedirect.com/science/article/pii/002219968390017X). Journal of International Economics, 14(1–2), 3–24.

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

[29] Andersen, T. G. and Bollerslev, T. and Diebold, F. X. and Labys, P. (2003). [Modeling and Forecasting Realized Volatility](https://doi.org/10.1111/1468-0262.00418). Econometrica, 71(2), 579–625.
