# Reliable Financial Forecasting Across Horizons and Volatility Regimes

Proposed doctoral research · Trần Anh Tuấn · 8 October 2026

This proposal builds on three original forecasting notebooks in the [repository](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/README.md). Existing project results are summarised in [preliminary results](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/docs/preliminary_results.md). The [Word copy](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/docs/proposals/PhD_Research_Proposal_Tran_Anh_Tuan.docx) contains the same substantive text. The common benchmark and new calibration methods below are proposed work.

## Abstract

I propose to investigate when daily financial forecasts generalise across forecast horizons and volatility regimes, and how their uncertainty can be calibrated when market conditions change. My current portfolio comprises three practical projects: VN30 price forecasting with NeuralProphet, Bitcoin daily Low forecasting with a TensorFlow attention model, and BID stock forecasting with robust weighted scikit-learn ExtraTrees. The notebooks contain saved predictions, plots and error metrics, but their evaluation designs differ. The Bitcoin run reports 3.40% MAPE for thirty one-step forecasts; NeuralProphet reports 9.72% raw and 5.75% smoothed MAPE, with smoothing tuned on the scored outcomes; BID reports 1.229% in the final window and 3.706% across three windows versus a 3.552% baseline mean. These observations motivate a research problem rather than establish model superiority. The doctoral work will use documented data, chronological model selection, matching forecast origins and prospective windows to compare forecasting strategies, then investigate interval coverage and width across volatility regimes.

## 1. Motivation and scope

A financial price forecast can appear close to the realised path while failing to improve on persistence. Different forecast origins can also produce superficially similar metrics for different tasks: updating a one-day forecast after each observed day is not the same experiment as predicting a full month from one origin. My existing projects expose both issues and provide concrete implementations to study them.

The initial scope is daily VN30, BTC-USD Low and BID. Each instrument will retain a clearly defined target and calendar. Comparisons will be within the same instrument and target before any cross-series summary. Trading profitability is not an objective of the initial study. A report that communicates forecast evidence is a possible later extension, conditional on reliable numerical results.

## 2. Related work and research opportunity

### 2.1 Evaluation and financial benchmarks

Rolling-origin evaluation makes the information available at prediction time explicit [1, 3]. Hewamalage et al. [4] discuss how preprocessing, splits and benchmark choices can distort conclusions. Hyndman and Koehler [2] motivate scaled errors alongside price errors. These sources determine the proposed protocol: chronological selection, matching origins, training-fitted scaling denominators and complete reporting.

Meese and Rogoff [10] study exchange-rate prediction; Welch and Goyal [11] study out-of-sample equity-premium prediction. Their targets differ from this portfolio, so their findings cannot be transferred directly to VN30, BID or Bitcoin Low. They motivate treating persistence and drift as serious competitors and retaining negative results.

Diebold and Mariano [5] provide a framework for predictive-loss comparison, with small-sample considerations discussed by Harvey et al. [6]. Overlapping multi-step errors require dependence-aware treatment; the stationary bootstrap [8] is a relevant alternative. Holm correction [7] can control a predeclared comparison family. A model confidence set [9] is a possible extension if a larger benchmark becomes justified. Comparisons will use matched loss series at a fixed horizon, rather than treating horizons from one origin as independent experiments.

### 2.2 Implemented model families

NeuralProphet [12] supplies a decomposable neural workflow with autoregression. Attention [13] motivates components of my TensorFlow regressor; the notebook implements a task-specific model rather than the complete original Transformer. Extremely randomized trees [14] underpin the scikit-learn workflow. These references explain the components; adopting a library or architecture is research preparation rather than a new methodological contribution.

The existing models have different features and prediction strategies. Matched-input comparisons and practical model-specific configurations will be assessed separately, with feature, direct-versus-recursive and smoothing ablations. This will distinguish architecture effects from additional predictors and postprocessing.

### 2.3 Intervals under dependence and changing distributions

Proper scoring rules [15] motivate evaluating interval width and missed outcomes together. Conformalized quantile regression [16] supplies a quantile-based comparator. The conformal introduction [17] explains exchangeability in standard marginal-coverage statements. Financial dependence and distribution change require examining those assumptions.

Barber et al. [18] establish limits on distribution-free conditional inference; their later work [19] studies departures from exchangeability. This proposal targets empirical coverage in a finite set of predefined volatility groups with explicit assumptions. Exact conditional coverage for every market state is not promised.

ACI [20], its online extension [21], EnbPI [22] and adaptive aggregation [23] provide competitors with different update rules and residual construction. Experiments will examine their behaviour when multi-step outcomes arrive with delay. Long-run average, local and volatility-group coverage will be reported separately.

### 2.4 Bounded research opportunity

The opportunity is to investigate the interaction of horizon, volatility change and delayed calibration feedback in documented financial experiments. The study will first determine whether the portfolio's price accuracy survives matching baselines and independent selection, then assess whether horizon-specific adaptation improves regime coverage at a useful width.

Novelty must be established against the literature during supervision. The distinction between marginal and regime coverage is already known. A contribution would identify a reproducible failure mechanism, test a targeted adaptation and establish when its benefit survives ablations and prospective evaluation.

## 3. Research questions and falsifiable hypotheses

**RQ1.** Under matching information sets and chronological evaluation, when do decomposable neural, attention-based and tree-based forecasts improve on persistence across horizons and volatility regimes?

**H1.** Some apparent price-accuracy advantages will shrink once baselines, origins and selection rules are matched. Tests will use per-origin loss differences at predeclared horizons, within an instrument and target. One favourable segment will not establish improvement.

**RQ2.** Can horizon-specific sequential calibration improve coverage within predefined volatility regimes at a useful width, compared with static, rolling and established adaptive methods?

**H2.** Volatility-normalised residuals and horizon-specific updates will reduce persistent miscoverage after volatility changes relative to pooled static calibration. The hypothesis fails if gains depend on excessive width, unstable groups or final-segment tuning.

Null results, weak effects and conditions favouring simpler methods will be retained. These are working hypotheses, and no new architecture or calibration guarantee is claimed as completed.

## 4. Existing preparation and preliminary evidence

The three original notebooks demonstrate data loading, feature construction, model implementation, evaluation and future forecasting. Original saved outputs are retained in the public copies. Publication edits add scope notes and portable setup/data paths; the BID copy reads an externally supplied CSV instead of its embedded raw-data payload.

**VN30 / NeuralProphet.** The saved run uses 4,408 source rows through 4 September 2026, reindexed to a weekday grid. It fits autoregression with 120 lags and a direct 30-step output. On the final thirty weekday rows, raw MAPE is 9.72%, MAE 187.88 and RMSE 218.17 index points. The anchored and smoothed path reports MAPE 5.75%, MAE 111.63 and RMSE 138.13. Smoothing is searched on the same scored outcomes, so this is retrospective tuning evidence. Holiday filling also means the steps are not necessarily exchange sessions.

**BTC-USD Low / TensorFlow.** The saved run uses 4,397 raw daily rows through 30 September 2026, with 4,368 feature-complete rows. A 180-day input window feeds a positional-encoding and multi-head-attention regressor. RobustScaler is fitted on training data. Thirty held-out one-step predictions report MAPE 3.40%, MAE USD 2,702.68 and RMSE USD 3,138.98; each prediction uses realised observations through the previous day. Training callbacks monitor training loss, with no separate validation segment in this run. The later recursive future path holds non-Low features fixed and has not been evaluated by that metric.

**BID / scikit-learn ExtraTrees.** The saved snapshot contains 3,153 observations through 24 September 2026. Five configurations are checked on eight validation windows, followed by three 30-observation test windows. ExtraTrees MAPE is 3.197%, 6.691% and 1.229%; zero-return baseline MAPE is 2.269%, 7.260% and 1.128%. The corresponding means are 3.706% and 3.552%. Mean daily direction accuracy is 38.889%; the composite selection loss is 0.968 relative to baseline 1.000. The model improves that composite measure while not improving average price MAPE. Previously inspected history and flagged data issues limit generalisation claims.

These experiments establish practical preparation and motivate better evaluation. They do not constitute a unified benchmark, statistical evidence of superiority or a prospective validation. The separately numbered supplementary study provides optional tested infrastructure; its results are not pooled with these original scores or treated as certification of the primary models.

## 5. Proposed methodology

### 5.1 Data and temporal protocol

The author has confirmed Investing.com as the source of the supplied VN30 and BID CSVs; source pages and hashes appear in the [data card](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/docs/data.md). Retrieval dates, adjustments and redistribution rights remain to be documented. The supplied 4,426-row VN30 file differs from the 4,408-row NeuralProphet snapshot. Date and OHLC anomalies will be reconciled before freezing research data.

For origin t, the primary endpoint is the target at t+h; horizons 1, 5, 20 and 30 are proposed. Equity/index steps will use validated exchange observations; Bitcoin will use daily observations. Endpoint forecasts and full paths will be assessed separately. Price and daily Low are different targets, so pooled MAPE will not establish cross-instrument rankings.

Chronological fitting, validation, calibration and final evaluation segments will be used. Examples whose labels cross a stage boundary will be excluded from that stage. Transformations, feature selection and volatility thresholds will use only information available at the origin. Refit schedules and compute budgets will be specified [1, 3, 4]. A prospective segment will be reserved after protocol freeze because existing history has been inspected; its stopping rule will precede outcome inspection.

### 5.2 Point forecasts and ablations

Persistence and drift will be established first, followed by the three model families on matching tasks and origins. Rolling one-step, direct multi-step and recursive forecasts remain distinct experiments. Updates will follow the declared comparison schedule.

Ablations will examine common versus model-specific features, direct versus recursive targets, validation-selected smoothing, and BID weighting and robustification. Neural early stopping will use chronological validation. Seed sensitivity, fit time and resources will be recorded. Settings will be frozen before final evaluation, with failed runs retained.

MAE, RMSE and MASE will be reported, using a training-fitted MASE denominator [2]. Relative MAE against matching persistence is a separate measure. Price MAPE is secondary and will not be applied to near-zero returns. Direction accuracy will include a baseline. Forecast error will not imply trading profitability.

### 5.3 Interval methods and candidate adaptation

At 80% and 95% nominal coverage, comparisons will begin with static and rolling residual calibration and ACI [20]. EnbPI [22], adaptive aggregation [23], online adaptation [21] and conformalized quantile regression [16] will be considered where estimator and compute requirements fit. Implementations and assumptions will be audited; published guarantees and observed financial performance will be distinguished.

The candidate adaptation combines horizon-specific residual histories, past-volatility scaling and separate update schedules. It is proposed work. An origin-t residual for horizon h enters calibration only after t+h is observed. Earlier evaluation outcomes may update calibration under the frozen prequential rule; they will never retune hyperparameters or redefine groups.

Volatility groups will use trailing realised returns and earlier-data thresholds, selected on validation and then frozen. Coverage, width and interval score [15] will be reported by horizon, group and time block, with sample counts. Sparse groups will be inconclusive rather than regrouped after outcome inspection. Universal distribution-free conditional guarantees will not be asserted [18, 19].

Ablations will remove volatility normalisation, horizon separation and adaptive updates in turn. Synthetic shifts will help isolate delayed-feedback failures and supplement financial evidence. Any theoretical analysis will state dependence and score assumptions and identify the coverage quantity controlled.

### 5.4 Statistical assessment

Matched per-origin losses at a fixed horizon form the comparison unit. Dependence-aware bootstrap intervals [8] and suitably specified accuracy tests [5, 6] will be considered, documenting overlap and block-length sensitivity. Three BID origins and one VN30 multi-step origin are insufficient for broad superiority claims.

A small primary comparison family will be predeclared, with Holm adjustment where appropriate [7]. Secondary analyses will be exploratory. A model confidence set [9] is optional if a larger benchmark is justified. Effect sizes, uncertainty and the coverage–width trade-off will be reported. Replication on another period or instrument will follow a stable initial design.

## 6. Intended contributions, feasibility and risks

**Empirical contribution.** Evidence of which portfolio conclusions survive matching origins, persistence, independent selection and volatility changes, including conditions favouring simpler models.

**Methodological contribution.** A tested horizon-specific calibration adaptation, or a supported account of why established methods suffice. Novelty and theoretical results depend on the literature review and supervision.

**Reproducibility contribution.** Versioned acquisition instructions, hashes, calendar decisions, frozen specifications and complete point/interval tables, with raw data distributed only when permitted.

Three working implementations provide practical preparation. The supplementary utilities require review, including their quantile convention, before reuse in interval research. Separate environments and training cost will be documented. Reliable baselines will precede expensive neural sweeps.

Risks include revisions, calendar errors, sparse volatility groups, unstable training and insufficient prospective observations. Responses include snapshot reconciliation, predeclared evidence requirements, seed variation, a smaller comparison family and explicit inconclusive findings. Additional assets and a reporting interface are optional.

## 7. Proposed plan

**Year 1.** Complete the literature review, data provenance and calendar checks. Freeze a common evaluation specification, add matching baselines to the primary workflows and reserve a prospective evaluation window.

**Year 2.** Evaluate direct, recursive and rolling strategies across horizons and volatility regimes. Run feature/postprocessing ablations and report null results as well as improvements.

**Year 3.** Develop and compare horizon-specific interval calibration, including delayed feedback and regime coverage. Replicate the main findings on additional documented periods or instruments if feasible.

**Year 4.** Independent replication, release of reproducible artefacts and thesis writing. An evidence-checked reporting interface is an optional extension after the forecast and calibration experiments are stable.

The order and duration will be adapted to programme requirements and supervision. A minimum viable thesis prioritises the two research questions and excludes optional reporting work if it distracts from reliable evaluation.

## 8. Reproducibility and limitations

Publish code, environment records, split dates, baseline definitions, selection rules, data cards and complete result tables. Redistribute raw data only with permission; otherwise record acquisition instructions and hashes. Keep synthetic smoke tests separate from financial accuracy evidence. Public saved outputs are informative but are not proof that rerunning a live download will produce identical numbers.

The current projects use different data snapshots and protocols; source attribution is confirmed by the author, while retrieval records, rights and adjustments remain incomplete; NeuralProphet smoothing uses the reported outcomes; BTC lacks a separate validation split; BID history was inspected earlier and has data flags. Addressing these limits is part of the proposed research. This document is a doctoral research draft, not a finished contribution or an agreed supervision.

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
