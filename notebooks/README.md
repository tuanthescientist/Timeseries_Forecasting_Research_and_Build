# Exploratory notebook catalogue

These selected historical notebooks show model development across assets. **They have not been rerun or validated end to end for this release.** They are separate from the tested NumPy benchmark.

Run notebook kernels with `notebooks/exploratory/` as the working directory. Keep market data in `data/raw/`; BTC and BNB cache paths are relative to that directory. VN30 examples expect `vn30.csv` (or `Data_VN30.csv` for NeuralProphet), using their original OHLCV column schemas. Configure the loader for your source before running.

## Selected experiments

| Notebook | Scope | Expected libraries (versions not reconstructed) |
| --- | --- | --- |
| [btc_lightgbm.ipynb](exploratory/btc_lightgbm.ipynb) | Bitcoin / LightGBM | lightgbm, pandas, numpy, scikit-learn, requests, matplotlib |
| [btc_neuralprophet.ipynb](exploratory/btc_neuralprophet.ipynb) | Bitcoin / NeuralProphet and CatBoost | neuralprophet, catboost, python-binance, pandas, numpy, scikit-learn, matplotlib |
| [bnb_neuralprophet.ipynb](exploratory/bnb_neuralprophet.ipynb) | BNB / NeuralProphet and CatBoost | neuralprophet, catboost, python-binance, pandas, numpy, scikit-learn, matplotlib |
| [btc_chronos.ipynb](exploratory/btc_chronos.ipynb) | Bitcoin / Chronos | chronos-forecasting, torch, python-binance, pandas, numpy, matplotlib, tqdm |
| [vn30_autoarima.ipynb](exploratory/vn30_autoarima.ipynb) | VN30 / AutoARIMA | sktime, pmdarima, pandas, numpy, scikit-learn, matplotlib |
| [vn30_catboost.ipynb](exploratory/vn30_catboost.ipynb) | VN30 / CatBoost | catboost, pandas, numpy, scikit-learn, matplotlib |
| [vn30_neuralprophet.ipynb](exploratory/vn30_neuralprophet.ipynb) | VN30 / NeuralProphet | neuralprophet, pandas, numpy, matplotlib |
| [btc_recurrent_low.ipynb](exploratory/btc_recurrent_low.ipynb) | Bitcoin low / recurrent networks | tensorflow, pandas, numpy, scikit-learn, pandas-datareader, yfinance, matplotlib, pillow, tqdm |
| [gold_recurrent_close.ipynb](exploratory/gold_recurrent_close.ipynb) | Gold close / recurrent networks | tensorflow, pandas, numpy, scikit-learn, pandas-datareader, yfinance, matplotlib, pillow, tqdm |

## Execution and interpretation

Use separate virtual environments for heavy model families. The table is an import-based dependency inventory, not a tested lockfile. Some models download weights or request live provider data, require internet access, and may require substantial memory. Inspect installation cells and configuration before execution.

The retained `btc_features.py` supports some historical notebooks. It is not part of the tested benchmark: callers must verify input column availability, forecast horizon, ordering, and train/test boundaries.

The gold notebook includes several calibration experiments using held-out observations. Those adjusted scores are not untouched final-test estimates. Inspect calibration cutoffs before making any comparison. Forecast bands in historical plots should not be interpreted as validated probability intervals.

## Publication transformations

Outputs, execution counts, and incidental metadata were removed; an explicit status cell was added. Absolute VN30 paths and BTC/BNB cache paths were replaced with relative paths. An unsupported 'highest accuracy' comment was removed from the Chronos copy. Remaining code and original comments are retained for inspection. Other experimental copies remain in the local workspace.

The [source manifest](../docs/source_manifest.json) records hashes for both original and published files. [Research audit](../docs/research_audit.md) documents known limitations.
