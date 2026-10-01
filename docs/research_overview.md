# Research overview

## Motivation

Financial prices provide a demanding setting for studying temporal generalization:
observed patterns can change, multi-step errors can accumulate, and evaluation can be
distorted when future observations affect features or calibration. This portfolio
organizes an existing set of forecasting experiments around a reproducible comparison.

## Scope and evidence

The historical work covers cryptocurrency daily prices (BTC and BNB), Vietnamese equity
index data (VN30), and gold. The notebooks contain model development and plotting code
for statistical, boosting, recurrent, and pretrained approaches. This release adds a
small benchmark, temporal integrity tests, provenance tracking, and an explicit protocol.

The checked-in results demonstrate software execution on a synthetic series. They do
not establish predictability in those markets or superiority of a model family. The
historical notebook outputs were removed; their numerical claims have not been adopted
as validated results. No publication, scholarship, institutional affiliation, or novel
algorithm is implied by this repository.

## Proposed experiment sequence

1. **Data specification:** identify provider, instrument, target (low/close/high),
   frequency, time zone, adjustment policy, download date, and immutable file hash.
2. **Baseline study:** compare persistence, drift, and the direct ridge model on
   identical origins. Keep a later period untouched during development.
3. **Model extensions:** implement one notebook model at a time against the same
   interface. Log dependencies, compute cost, seeds, failures, and predictions.
4. **Ablations:** compare price versus return targets, lag-only versus volume features,
   and training-window choices using a development period.
5. **Final assessment:** freeze choices, evaluate the untouched period, report errors
   by horizon and regime, and analyze dependence between overlapping forecasts.
6. **Uncertainty study:** test calibrated intervals using earlier calibration data and
   later coverage measurements, with attention to regime changes.

## Questions suitable for further doctoral research

- How do pretrained time-series models transfer across asset classes and regimes?
- Can uncertainty estimates remain calibrated when the generating process changes?
- When do interpretable lag features match more complex neural architectures?

These questions describe possible extensions. Answering them requires controlled
experiments beyond this release, including disclosure of foundation-model pretraining
overlap where it can be established.
