# Attention timing pilot — preparation only

Status: not run. This plan measures resource requirements; it does not establish forecasting accuracy or freeze the Stage B model. No measured fit time is available yet. The proposal timing scenarios remain assumptions.

## Scope and gates

Use a standalone pilot rather than executing the archived notebook end to end. Its original run includes already inspected historical evaluation data and saved forecasting outputs. Keep the original notebook unchanged.

Before fitting, resolve the exact causal feature list, architecture, horizon strategy and label cutoffs. Fit transformations only on training observations. All pilot fitting/validation labels must end by 2023-06-30, using the declared chronological training/validation splits. Do not inspect retrospective test losses to choose a pilot configuration.

The archive provides a starting configuration: build_refined_model_v3, Adam learning rate 8e-5 with clipnorm 1.0, Huber loss delta 1.0, batch size 32 and maximum 250 epochs. These values are notebook evidence, not a newly approved full-study specification. Early-stopping monitor/patience and complete model/feature settings must be recorded before execution.

## Initial timing configuration

Begin with seed 42 and the 180-day input window, using a one-step target and the fully recorded pilot architecture/features. Record compilation/startup separately from epoch and full-fit times. If authorised, cap the whole pilot at 15 minutes with an external timeout, including setup. A run stopped by this cap is censored: it cannot be reported as the duration of a completed 250-epoch or early-stopped fit.

A single short run only supplies an initial timing observation. A useful budget subsequently needs both 90/180-day windows, representative expanding training sizes and direct/recursive training configurations. Measure seed variability and memory before assuming parallel speed-up.

## Required timing record

- Source commit, snapshot hash, pilot configuration hash and feature list.
- Hardware and CPU/GPU identity, TensorFlow/CUDA versions and observed device placement.
- Dates, sample count, window, horizon, seed, batch size, optimiser and stopping rule.
- Compilation time, completed epochs, per-epoch times, total wall time and peak memory.
- Completion versus timeout/failure and any recovery steps.

No nvidia-smi command was found in the current shell on 8 October 2026. This does not prove that no GPU exists. Confirm device access before making a GPU-runtime claim. A CPU timing result cannot be labelled a GPU benchmark.

## Budget decision

The full-grid scenario is 34 × 2 × 3 × 6 = 1,224 fits; identical recursive/rolling training could reduce it to 1,020 through explicit reuse. Add validation search, calibration fits, ablations, retries, inference and future refits separately. Extrapolation must account for expanding training sizes and completed-epoch variation.

Review measurements and actual device availability by 16 October. If representative timings are unavailable, the feasibility gate remains unresolved. Delay Stage B or amend the schedule rather than treating assumed minutes-per-fit as evidence. See the [proposal](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/docs/proposal.md).
