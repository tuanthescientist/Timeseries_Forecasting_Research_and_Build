# Financial Time-Series Forecasting: Three Notebook Projects

A forecasting portfolio built around three original notebooks: **VN30 with NeuralProphet, Bitcoin daily Low with TensorFlow, and BID stock with scikit-learn ExtraTrees**. Each notebook contains its model, evaluation, saved forecasts and plots, and a future forecasting workflow.

Maintained by [Tuan Tran](https://github.com/tuanthescientist). MIT licensed code. These are exploratory projects that demonstrate implementation and evaluation experience; the saved metrics have different targets and evaluation designs.

## Start with these three notebooks

| Project | Notebook | Saved price MAPE | How to interpret it |
| --- | --- | ---: | --- |
| VN30 · NeuralProphet | [vn30-forecast-neuralprophet.ipynb](notebooks/vn30-forecast-neuralprophet.ipynb) | Raw **9.72%**; smoothed **5.75%** | One direct 30-step forecast; smoothing is tuned on the same evaluation outcomes. |
| Bitcoin Low · TensorFlow | [btc-low-forecast-tensorflow.ipynb](notebooks/btc-low-forecast-tensorflow.ipynb) | **3.40%** | Thirty rolling one-step forecasts, each using actual history through the previous day. |
| BID · scikit-learn | [stock-forecast-sklearn.ipynb](notebooks/stock-forecast-sklearn.ipynb) | Last window **1.229%**; three-window mean **3.706%** | Baseline MAPE is 1.128% and 3.552%, respectively; low price error alone does not show baseline improvement. |

The values are transcribed from the original saved runs, not rerun for this release. They should not be ranked against one another: instruments, targets, snapshots and forecast origins differ. [Full metric details](docs/preliminary_results.md) include MAE, RMSE, all BID test windows and the limits of each score.

For a quick review, open the three notebooks above and read their introductory notes, model cells, evaluation tables and forecast plots. For a deeper review, read [evaluation designs](docs/evaluation.md), the [data card](docs/data.md), then the [doctoral research proposal](docs/proposals/PhD_Research_Proposal.md) ([Word copy](docs/proposals/PhD_Research_Proposal_Tran_Anh_Tuan.docx)). The [repository guide](docs/reading_guide.md) explains the workflows and how to inspect the evidence.

## What each project demonstrates

**NeuralProphet / VN30.** Autoregression with 120 lags, trend and seasonality, and direct 30-step prediction. The notebook compares the raw forecast with continuity anchoring, EMA smoothing and volatility caps. The smoothed result is exploratory postprocessing selected on the reported segment. A weekday calendar fills holiday gaps.

**TensorFlow / Bitcoin Low.** A custom attention-based regressor uses 180 days of inputs, price and volume indicators, positional encoding, two multi-head attention blocks, Conv1D projections, pooling and a dense head. RobustScaler is fitted on the training segment. Saved test predictions use real preceding observations. The separate future path recursively replaces Low while holding the other features fixed.

**scikit-learn / BID.** A robust weighted ExtraTrees model uses 32 causal features and direct 30-step return targets. Five configurations are evaluated on eight validation windows; the selected configuration is reported on three test windows alongside zero-return persistence. The notebook includes data checks, error and direction metrics, training audits and CSV exports.

## Run the primary notebooks

Open the saved notebooks on GitHub without installing anything. To rerun, use a **separate Python environment and Jupyter kernel for each project**; their original setup cells install different packages. The supplementary package and its lock file do not lock these three environments.

| Notebook | Setup and data |
| --- | --- |
| NeuralProphet | Run the installation cell once, restart the kernel, then skip installation. It pins NeuralProphet 0.8.0. Supply the original Date/Price CSV at data/raw/vn30.csv or set VN30_CSV; the Kaggle path is a fallback. |
| TensorFlow | Saved run: TensorFlow 2.19.0. Install tensorflow==2.19.0, numpy, pandas, scikit-learn, matplotlib, Pillow, tqdm, yfinance and pandas-datareader. The setup cell installs TensorFlow if missing. Yahoo Finance download requires internet and uses the current date; rerun scores can change. |
| scikit-learn | Run setup once and restart if necessary. It pins scikit-learn 1.8.0. Supply the original OHLCV CSV at data/raw/bid.csv or set BID_CSV; the Kaggle path is a fallback. Exports go to ignored results/local/bid-extratrees/. |

Market CSVs and model weights are not bundled. The BID publication copy reads an external CSV instead of the embedded raw-data payload in the source notebook. Read [data provenance and snapshot limits](docs/data.md) before trying to reproduce the exact saved values. Primary models have not been retrained in CI.

## Repository layout

```text
notebooks/
  vn30-forecast-neuralprophet.ipynb    primary: VN30 / NeuralProphet
  btc-low-forecast-tensorflow.ipynb    primary: BTC Low / TensorFlow
  stock-forecast-sklearn.ipynb         primary: BID / scikit-learn
  supplementary/                     separate numbered evaluation notebooks 01–03
docs/
  data.md                            primary-project data and provenance
  evaluation.md                      three distinct evaluation designs
  preliminary_results.md             original saved metrics with limitations
  reading_guide.md                    workflows and reviewer reading route
  proposals/                         proposed PhD research, Markdown and Word
  supplementary/                     separate study guide, protocol and results
src/tsresearch/, configs/, tests/     infrastructure for the supplementary study
results/vn30/, results/bid/           supplementary study tables and figures
data/demo/                           synthetic input for supplementary smoke runs
data/raw/, results/local/            ignored local data and generated outputs
scripts/                             repository checks and supplementary runner
```

The numbered notebooks were added during repository restructuring and are **supplementary**, not renamed versions of the three original projects. Their source, tests and results are retained for optional further study. See the [supplementary guide](docs/supplementary/README.md). Earlier explorations remain on [archive/v0.1-exploratory](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/tree/archive/v0.1-exploratory) (tag v0.1.0).

## Checks and supplementary execution

```bash
python -m pip install -c requirements-lock.txt -e ".[dev]"
ruff check .
python -m unittest discover -s tests -v
python scripts/check_repository.py
python scripts/run_notebooks.py   # numbered supplementary notebooks only
```

CI checks repository links and all six notebook files, runs unit tests for the supplementary package, and executes the three supplementary notebooks on synthetic data. Passing CI does not validate the original three forecasting metrics. The primary notebooks are run manually with their own dependencies and market data.

## Research direction

The [proposal](docs/proposals/PhD_Research_Proposal.md) starts from these three practical workflows and asks how model comparisons and uncertainty estimates hold up across horizons and volatility regimes. A common evaluation protocol, untouched future windows, data provenance, baselines and interval calibration are proposed next steps. Completed notebook outputs and proposed doctoral contributions are identified separately.

See [CITATION.cff](CITATION.cff) when citing the repository; include the exact commit.
