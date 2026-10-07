# Repository and notebook reading guide

## A reviewer's route

Start with the README's three-project table. Open one primary notebook and read its opening scope note before its graphs. Inspect the data loader and target, the split and what each forecast can observe, the model, then the metric table and baseline. Read the other two notebooks in the same way. Follow [saved results](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/docs/preliminary_results.md) and [evaluation designs](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/docs/evaluation.md) for the limits, and finally the [proposal](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/docs/proposals/PhD_Research_Proposal.md) to see how the practical projects lead to proposed research.

A professor can assess code comprehension, implementation breadth, experimental reasoning and honesty about limits from this route. The metric is one part of that assessment. A clear explanation of why a forecast has access to a particular observation matters as much as a visually close prediction line. The supplementary study is optional and should not be presented as one of the applicant's three original projects.

## VN30 workflow

CSV → Date/Price cleaning → weekday reindex and gap filling → NeuralProphet with 120 lags and 30 direct outputs → raw final-window forecast → anchoring, EMA and volatility caps → smoothing search on those final outcomes → raw/smoothed errors and plots → full-history future forecast.

The model-training and smoothing stages solve different problems. Explain the trend/seasonality/autoregression settings, how one origin emits multiple horizons, and why choosing smoothing with the scored outcomes limits the 5.75% result. The source data end and the weekday calendar are visible in saved outputs.

## Bitcoin workflow

Live Yahoo download → Low-based technical and volume features → final 30-day split → RobustScaler fitted on train → 180-day windows → positional encoding and attention regressor → training-loss callbacks → fixed-model one-step test predictions with realised previous days → USD error metrics → separate recursive 30-day future path.

Explain the input tensor (samples, 180 days, 11 features in the saved run), what attention and pooling do in this specific architecture, and the inverse transform. Distinguish the held-out one-step test from the training prediction diagnostic and from the recursive future path, whose other features are held constant. This implementation's active model is attention-based; imports alone do not make it an LSTM model.

## BID workflow

External original CSV → data-quality checks → 32 causal features → five model configurations on eight validation windows → frozen selection → robust/time-weighted ExtraTrees at three test origins → 30 direct return outputs → reconstructed prices → model-versus-zero-return errors, direction scores and audit tables → future 30-step forecast and local CSV exports.

Explain the weighting, training window, minimum leaf size, joint targets and selection weights. Show all three test windows: the last-window 1.23% MAPE is attractive as a price error, while the baseline's 1.128% and mean results constrain any superiority claim. The original Vietnamese notes already describe these limits.

## How the repository runs

The primary notebooks contain their own workflows and do not import tsresearch. Use a separate environment/kernel for each because their setup versions differ. They need real input data or internet access and are rerun manually.

The separate numbered study imports src/tsresearch, reads configs and writes aggregate results. Its runner defaults to notebooks/supplementary/; its synthetic mode supports CI. The package tests concern those modules. Notebook-format and link checks inspect all six published notebooks. Neither synthetic execution nor unit tests retrain or verify the primary neural models' accuracy.

The proposal distinguishes existing saved experiments from proposed common evaluation, new prospective evidence and interval research. It should be adapted to a potential supervisor's topic and application requirements before submission.
