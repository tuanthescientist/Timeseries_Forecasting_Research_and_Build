# Reliable Financial Forecasting Across Horizons and Volatility Regimes

Proposed doctoral research · Trần Anh Tuấn · 7 October 2026

This proposal builds on three original forecasting notebooks in the [repository](../../README.md). Existing project results are summarised in [preliminary results](../preliminary_results.md). The [Word copy](PhD_Research_Proposal_Tran_Anh_Tuan.docx) contains the same substantive text. The common benchmark and new calibration methods below are proposed work.

## Abstract

I propose to investigate when daily financial forecasts generalise across forecast horizons and volatility regimes, and how their uncertainty can be calibrated when market conditions change. My current portfolio comprises three practical projects: VN30 price forecasting with NeuralProphet, Bitcoin daily Low forecasting with a TensorFlow attention model, and BID stock forecasting with robust weighted scikit-learn ExtraTrees. The notebooks contain saved predictions, plots and error metrics, but their evaluation designs differ. The Bitcoin run reports 3.40% MAPE for thirty one-step forecasts; NeuralProphet reports 9.72% raw and 5.75% smoothed MAPE, with smoothing tuned on the scored outcomes; BID reports 1.229% in the final window and 3.706% across three windows versus a 3.552% baseline mean. These observations motivate a research problem rather than establish model superiority. The doctoral work will use documented data, chronological model selection, matching forecast origins and prospective windows to compare forecasting strategies, then investigate interval coverage and width across volatility regimes.

## 1. Motivation and scope

A financial price forecast can appear close to the realised path while failing to improve on persistence. Different forecast origins can also produce superficially similar metrics for different tasks: updating a one-day forecast after each observed day is not the same experiment as predicting a full month from one origin. My existing projects expose both issues and provide concrete implementations to study them.

The initial scope is daily VN30, BTC-USD Low and BID. Each instrument will retain a clearly defined target and calendar. Comparisons will be within the same instrument and target before any cross-series summary. Trading profitability is not an objective of the initial study. A report that communicates forecast evidence is a possible later extension, conditional on reliable numerical results.

## 2. Related work and research opportunity

NeuralProphet combines decomposable forecasting components with autoregression in a PyTorch framework [1]. It provides a practical contrast to the custom TensorFlow attention regressor and ExtraTrees workflow already implemented in this portfolio. Their existing notebook scores cannot be used to rank those model families because the tasks and evaluation origins differ.

Rolling-origin evaluation fits and scores using chronologically available observations; it can be designed for one-step or multiple-step horizons [2]. Forecast accuracy measures need careful interpretation, and scaled errors can support comparisons against simple benchmarks [3]. The first research opportunity is to determine which conclusions from these practical workflows survive comparable origins, baseline comparisons, independent selection windows and changes in volatility.

Adaptive conformal inference provides a starting point for calibration under distribution shift [4]. The second opportunity is empirical: compare horizon-specific calibration methods by both marginal coverage and coverage within predefined volatility regimes, while accounting for interval width and delayed availability of multi-step outcomes. Existing theoretical results will be reviewed before claiming a guarantee for any proposed adaptation.

## 3. Research questions

**RQ1.** Under matching information sets and chronological evaluation, when do decomposable neural, attention-based and tree-based forecasts improve on persistence across horizons and volatility regimes?

The working hypothesis is that apparent price accuracy will often shrink relative to persistence once forecast origins and selection rules are matched. Direct and recursive strategies may respond differently to horizon and regime changes. Negative or mixed findings will be retained.

**RQ2.** Can horizon-specific sequential calibration improve prediction-interval coverage within volatility regimes at a useful width, compared with static and rolling calibration?

The working hypothesis is that adaptation can reduce persistent miscoverage after a volatility change, but good average coverage will not necessarily imply good coverage inside each regime. Regime definitions and calibration choices will be fixed before a new final evaluation.

These questions define the proposed empirical and methodological work. No new forecasting architecture or calibration guarantee is claimed as already completed.

## 4. Existing preparation and preliminary evidence

The three original notebooks demonstrate data loading, feature construction, model implementation, evaluation and future forecasting. Original saved outputs are retained in the public copies. Publication edits add scope notes and portable setup/data paths; the BID copy reads an externally supplied CSV instead of its embedded raw-data payload.

**VN30 / NeuralProphet.** The saved run uses 4,408 source rows through 4 September 2026, reindexed to a weekday grid. It fits autoregression with 120 lags and a direct 30-step output. On the final thirty weekday rows, raw MAPE is 9.72%, MAE 187.88 and RMSE 218.17 index points. The anchored and smoothed path reports MAPE 5.75%, MAE 111.63 and RMSE 138.13. Smoothing is searched on the same scored outcomes, so this is retrospective tuning evidence. Holiday filling also means the steps are not necessarily exchange sessions.

**BTC-USD Low / TensorFlow.** The saved run uses 4,397 raw daily rows through 30 September 2026, with 4,368 feature-complete rows. A 180-day input window feeds a positional-encoding and multi-head-attention regressor. RobustScaler is fitted on training data. Thirty held-out one-step predictions report MAPE 3.40%, MAE USD 2,702.68 and RMSE USD 3,138.98; each prediction uses realised observations through the previous day. Training callbacks monitor training loss, with no separate validation segment in this run. The later recursive future path holds non-Low features fixed and has not been evaluated by that metric.

**BID / scikit-learn ExtraTrees.** The saved snapshot contains 3,153 observations through 24 September 2026. Five configurations are checked on eight validation windows, followed by three 30-observation test windows. ExtraTrees MAPE is 3.197%, 6.691% and 1.229%; zero-return baseline MAPE is 2.269%, 7.260% and 1.128%. The corresponding means are 3.706% and 3.552%. Mean daily direction accuracy is 38.889%; the composite selection loss is 0.968 relative to baseline 1.000. The model improves that composite measure while not improving average price MAPE. Previously inspected history and flagged data issues limit generalisation claims.

These experiments establish practical preparation and motivate better evaluation. They do not constitute a unified benchmark, statistical evidence of superiority or a prospective validation. The separately numbered supplementary study provides optional tested infrastructure; its results are not pooled with these original scores or treated as certification of the primary models.

## 5. Proposed methodology

**Data and protocol.** Record the provider, retrieval time, byte hash, adjustment policy, rights and calendar of every snapshot. Reconcile flagged source issues. Define targets and the information available at each origin. Use chronological fitting, model selection, calibration and final evaluation segments, separating boundaries where multi-step labels would otherwise cross them. Because the current history has been inspected, collect a new prospective evaluation window before making a stronger generalisation claim.

**RQ1 experiments.** Compare persistence and simple drift with NeuralProphet, the TensorFlow attention model and ExtraTrees on matching tasks. Evaluate one-step rolling forecasts separately from direct and recursive multi-step forecasts at predeclared horizons. Keep model-specific feature sets explicit; run controlled feature and postprocessing ablations rather than attributing every difference to the architecture. Select NeuralProphet smoothing, neural training choices and tree settings on validation data only. Freeze choices before the final window. Report all windows, failures, compute cost and seed variability where applicable.

**RQ2 experiments.** Construct residual-based intervals with static, rolling and adaptive calibration. Use a multi-step outcome only once its horizon has elapsed. Define volatility regimes from past information and earlier selection data, not future realised test errors. Compare both unnormalised and volatility-normalised residuals. Audit order-statistic and feedback conventions before implementing any claimed conformal correction. A calibration method will be judged by coverage and width together, rather than by average coverage alone.

**Metrics and uncertainty.** Report MAE, RMSE and scaled error relative to a training-fitted denominator, with price MAPE as a secondary descriptive measure. Do not use MAPE on near-zero returns. Report performance relative to matching persistence, per-horizon errors and regime-specific scores. Interval evaluation includes 80% and 95% coverage, mean width and interval score. Estimate uncertainty in loss differences using a dependence-aware resampling design, and predeclare comparison families and any multiplicity correction.

## 6. Intended contributions and practical feasibility

The intended outputs are a reproducible comparison of forecast strategies under matching information sets, an empirical account of where apparent accuracy survives baseline and regime checks, and a horizon-specific calibration approach or documented boundary showing where simpler intervals are preferable. Novelty will be refined with the literature review and the potential supervisor; the existing notebook implementations are preliminary preparation.

The project begins with three working model workflows and saved evidence that I can explain in detail. The supplementary Python package provides reusable temporal-evaluation utilities and tests, but requires review before integrating it with the primary projects. Separate dependency environments and model training costs will be recorded. No GPU-heavy sweep is needed before establishing reliable baseline experiments.

## 7. Proposed plan

**Year 1.** Complete the literature review, data provenance and calendar checks. Freeze a common evaluation specification, add matching baselines to the primary workflows and reserve a prospective evaluation window.

**Year 2.** Evaluate direct, recursive and rolling strategies across horizons and volatility regimes. Run feature/postprocessing ablations and report null results as well as improvements.

**Year 3.** Develop and compare horizon-specific interval calibration, including delayed feedback and regime coverage. Replicate the main findings on additional documented periods or instruments if feasible.

**Year 4.** Independent replication, release of reproducible artefacts and thesis writing. An evidence-checked reporting interface is an optional extension after the forecast and calibration experiments are stable.

The order and duration will be adapted to programme requirements and supervision. A minimum viable thesis prioritises the two research questions and excludes optional reporting work if it distracts from reliable evaluation.

## 8. Reproducibility and limitations

Publish code, environment records, split dates, baseline definitions, selection rules, data cards and complete result tables. Redistribute raw data only with permission; otherwise record acquisition instructions and hashes. Keep synthetic smoke tests separate from financial accuracy evidence. Public saved outputs are informative but are not proof that rerunning a live download will produce identical numbers.

The current projects use different data snapshots and protocols; source rights and adjustments are incomplete; NeuralProphet smoothing uses the reported outcomes; BTC lacks a separate validation split; BID history was inspected earlier and has data flags. Addressing these limits is part of the proposed research. This document is a doctoral research draft, not a finished contribution or an agreed supervision.

## References

[1] Triebe, O., Hewamalage, H., Pilyugina, P., Laptev, N., Bergmeir, C., and Rajagopal, R. (2021). NeuralProphet: Explainable Forecasting at Scale. arXiv:2111.15397. https://arxiv.org/abs/2111.15397

[2] Hyndman, R. J., and Athanasopoulos, G. Forecasting: Principles and Practice, 3rd edition, Section 5.10: Time series cross-validation. https://otexts.com/fpp3/tscv.html

[3] Hyndman, R. J., and Koehler, A. B. (2006). Another look at measures of forecast accuracy. International Journal of Forecasting, 22(4), 679–688. https://robjhyndman.com/publications/another-look-at-measures-of-forecast-accuracy/

[4] Gibbs, I., and Candès, E. (2021). Adaptive Conformal Inference Under Distribution Shift. Advances in Neural Information Processing Systems, 34. https://arxiv.org/abs/2106.00170
