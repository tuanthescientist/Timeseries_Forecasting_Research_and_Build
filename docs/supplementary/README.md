# Supplementary evaluation study

The primary portfolio is the three original [NeuralProphet](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/notebooks/vn30-forecast-neuralprophet.ipynb), [TensorFlow](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/notebooks/btc-low-forecast-tensorflow.ipynb) and [scikit-learn](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/notebooks/stock-forecast-sklearn.ipynb) notebooks. The numbered study below was added during repository restructuring in commit 7da3eb8; it is not a renamed or derived copy of those three projects.

| Notebook | Supplementary purpose |
| --- | --- |
| [01 Data and baselines](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/notebooks/supplementary/01_data_and_baselines.ipynb) | Data checks, temporal protocol and persistence/drift baselines |
| [02 Model comparison](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/notebooks/supplementary/02_model_comparison.ipynb) | Return forecasts from ridge, ExtraTrees and gradient boosting |
| [03 Uncertainty calibration](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/notebooks/supplementary/03_uncertainty_calibration.ipynb) | Static, rolling and adaptive interval-calibration experiments |

[Protocol](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/docs/supplementary/protocol.md), [data card](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/docs/supplementary/data.md) and [saved aggregate results](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/docs/supplementary/preliminary_results.md) describe only this study. Its code is in [src/tsresearch](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/tree/main/src/tsresearch), dates and paths are in [configs](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/tree/main/configs), and derived outputs are in [results/vn30](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/tree/main/results/vn30) and [results/bid](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/tree/main/results/bid). Keep these results separate from the original projects' scores.

## Execution

```bash
python -m pip install -c requirements-lock.txt -e ".[dev]"
python -m unittest discover -s tests -v
python scripts/run_notebooks.py
```

The runner executes only the numbered supplementary notebooks by default. The bundled VN30 and BID CSVs match the default configured paths. If they are absent, it uses synthetic data and announces demo mode. Set TSR_FORCE_DEMO=1 to force that mode; use --save only when intentionally replacing saved outputs. NeuralProphet and TensorFlow are not dependencies of this package.

These materials are optional exploratory infrastructure. They are not evidence that the original three models share this protocol or pass its temporal-integrity tests. Previously inspected histories and source-data issues remain documented. Numerical calibration conventions also require review before making a finite-sample conformal guarantee; the current quantile helper interpolates a corrected probability with the higher method rather than directly selecting the intended order statistic. Saved interval tables should be treated as exploratory and regenerated after such an audit.
