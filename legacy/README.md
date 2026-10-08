> Archived portfolio as of commit eb1eac0. These saved results are historical preparation and do not use the BTC research protocol at the repository root.

# Financial Time-Series Forecasting: From Three Projects to a Research Agenda

A forecasting portfolio built around three original notebooks: **VN30 with NeuralProphet, Bitcoin daily Low with TensorFlow, and BID stock with scikit-learn ExtraTrees**. Each notebook contains its model, evaluation, saved forecasts and plots, and a future forecasting workflow.

The research direction is to ask **when forecast accuracy survives matching baselines and horizons, and how prediction intervals respond to changing volatility**. The notebooks provide practical preparation; the proposal defines the experiments needed to answer those questions.

Maintained by [Tuan Tran](https://github.com/tuanthescientist). MIT licensed code. These are exploratory projects that demonstrate implementation and evaluation experience; the saved metrics have different targets and evaluation designs.

## Review the portfolio

| Reading route | Evidence to inspect |
| --- | --- |
| Orientation | This README: three projects, their scope and research direction |
| Implementation | Three primary notebooks: target, information at each origin, model and outputs |
| Experimental reasoning | [Evaluation designs](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/legacy/docs/evaluation.md) and [saved results](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/legacy/docs/preliminary_results.md): baselines and limits |
| Data credibility | [Data card](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/legacy/docs/data.md): provider, hashes and snapshot issues |
| Doctoral direction | [Proposal](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/legacy/docs/proposals/PhD_Research_Proposal.md): literature, hypotheses, methods and feasibility |
| Further reading | [Literature map](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/legacy/docs/references.md) and 23 linked proposal references |

## Three primary notebook projects

| Project | Notebook | Saved price MAPE | How to interpret it |
| --- | --- | ---: | --- |
| VN30 · NeuralProphet | [vn30-forecast-neuralprophet.ipynb](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/legacy/notebooks/vn30-forecast-neuralprophet.ipynb) | Raw **9.72%**; smoothed **5.75%** | One direct 30-step forecast; smoothing is tuned on the same evaluation outcomes. |
| Bitcoin Low · TensorFlow | [btc-low-forecast-tensorflow.ipynb](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/legacy/notebooks/btc-low-forecast-tensorflow.ipynb) | **3.40%** | Thirty rolling one-step forecasts, each using actual history through the previous day. |
| BID · scikit-learn | [stock-forecast-sklearn.ipynb](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/legacy/notebooks/stock-forecast-sklearn.ipynb) | Last window **1.229%**; three-window mean **3.706%** | Baseline MAPE is 1.128% and 3.552%, respectively; low price error alone does not show baseline improvement. |

The values are transcribed from the original saved runs, not rerun for this release. They should not be ranked against one another: instruments, targets, snapshots and forecast origins differ. [Full metric details](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/legacy/docs/preliminary_results.md) include MAE, RMSE, all BID test windows and the limits of each score.

For a quick review, open the three notebooks above and read their introductory notes, model cells, evaluation tables and forecast plots. For a deeper review, read [evaluation designs](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/legacy/docs/evaluation.md), the [data card](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/legacy/docs/data.md), then the [doctoral research proposal](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/legacy/docs/proposals/PhD_Research_Proposal.md) ([Word copy](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/legacy/docs/proposals/PhD_Research_Proposal_Tran_Anh_Tuan.docx)). The [repository guide](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/legacy/docs/reading_guide.md) explains the workflows and how to inspect the evidence.

## What each project demonstrates

**NeuralProphet / VN30.** Autoregression with 120 lags, trend and seasonality, and direct 30-step prediction. The notebook compares the raw forecast with continuity anchoring, EMA smoothing and volatility caps. The smoothed result is exploratory postprocessing selected on the reported segment. A weekday calendar fills holiday gaps.

**TensorFlow / Bitcoin Low.** A custom attention-based regressor uses 180 days of inputs, price and volume indicators, positional encoding, two multi-head attention blocks, Conv1D projections, pooling and a dense head. RobustScaler is fitted on the training segment. Saved test predictions use real preceding observations. The separate future path recursively replaces Low while holding the other features fixed.

**scikit-learn / BID.** A robust weighted ExtraTrees model uses 32 causal features and direct 30-step return targets. Five configurations are evaluated on eight validation windows; the selected configuration is reported on three test windows alongside zero-return persistence. The notebook includes data checks, error and direction metrics, training audits and CSV exports.

## Run the primary notebooks

Open the saved notebooks on GitHub without installing anything. To rerun, use a **separate Python environment and Jupyter kernel for each project**; their original setup cells install different packages. The supplementary package and its lock file do not lock these three environments.

| Notebook | Setup and data |
| --- | --- |
| NeuralProphet | Run the installation cell once, restart the kernel, then skip installation. It pins NeuralProphet 0.8.0. The bundled data/raw/vn30.csv is the newer 4,426-row snapshot. Set VN30_CSV for another snapshot; the Kaggle path is a fallback. |
| TensorFlow | Saved run: TensorFlow 2.19.0. Install tensorflow==2.19.0, numpy, pandas, scikit-learn, matplotlib, Pillow, tqdm, yfinance and pandas-datareader. The setup cell installs TensorFlow if missing. Yahoo Finance download requires internet and uses the current date; rerun scores can change. |
| scikit-learn | Run setup once and restart if necessary. It pins scikit-learn 1.8.0. The bundled data/raw/bid.csv matches the original snapshot. Set BID_CSV for another file; the Kaggle path is a fallback. Exports go to ignored results/local/bid-extratrees/. |

The author confirms that VN30 and BID CSVs were downloaded from Investing.com: [VN30 history](https://www.investing.com/indices/vn-30-historical-data) and [BID history](https://www.investing.com/equities/commercial-bank-investment-develop-historical-data). **Both supplied CSV snapshots are published:** [VN30 CSV](https://www.investing.com/) and [BID CSV](https://www.investing.com/). The VN30 file is newer than the snapshot behind the saved NeuralProphet metrics. Model weights are not bundled. The BID publication copy reads an external CSV instead of the embedded raw-data payload in the source notebook. Read [data provenance and snapshot limits](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/legacy/docs/data.md) before trying to reproduce the exact saved values. Primary models have not been retrained in CI.

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
data/raw/                           published vn30.csv and bid.csv snapshots
results/local/                      ignored generated outputs
scripts/                             repository checks and supplementary runner
```

The numbered notebooks were added during repository restructuring and are **supplementary**, not renamed versions of the three original projects. Their source, tests and results are retained for optional further study. See the [supplementary guide](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/legacy/docs/supplementary/README.md). Earlier explorations remain on [archive/v0.1-exploratory](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/tree/archive/v0.1-exploratory) (tag v0.1.0).

## Checks and supplementary execution

```bash
python -m pip install -c requirements-lock.txt -e ".[dev]"
ruff check .
python -m unittest discover -s tests -v
python scripts/check_repository.py
python scripts/run_notebooks.py   # numbered supplementary notebooks only
```

CI checks repository links and all six notebook files, runs unit tests for the supplementary package, and executes the three supplementary notebooks on synthetic data. Passing CI does not validate the original three forecasting metrics. The primary notebooks are run manually with their own dependencies and market data.

## Research status and direction

| Available evidence | Proposed doctoral work |
| --- | --- |
| Original model workflows and saved outputs | Matching tasks, origins and chronological comparison |
| Distinct designs with documented limits | Independent selection and prospective evaluation |
| BID persistence comparison and VN30 postprocessing | Common baselines and controlled ablations |
| Optional supplementary infrastructure | Audited intervals with delayed feedback and volatility-group analysis |

The [proposal](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/legacy/docs/proposals/PhD_Research_Proposal.md) starts from these three practical workflows and asks how model comparisons and uncertainty estimates hold up across horizons and volatility regimes. A common evaluation protocol, untouched future windows, data provenance, baselines and interval calibration are proposed next steps. Completed notebook outputs and proposed doctoral contributions are identified separately.

## Selected academic foundations

[Forecasting: Principles and Practice](https://otexts.com/fpp3/) and [forecast evaluation best practices](https://arxiv.org/abs/2203.10716) guide temporal evaluation. [NeuralProphet](https://arxiv.org/abs/2111.15397), [attention](https://arxiv.org/abs/1706.03762) and [ExtraTrees](https://doi.org/10.1007/s10994-006-6226-1) explain model components. Interval research builds on [ACI](https://arxiv.org/abs/2106.00170) and [adaptive conformal time-series methods](https://proceedings.mlr.press/v162/zaffran22a.html), with [conditional-coverage limits](https://arxiv.org/abs/1903.04684) explicitly considered. The [literature map](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/legacy/docs/references.md) connects all 23 references to research decisions.

See [CITATION.cff](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/legacy/CITATION.cff) when citing the repository; include the exact commit.

VN30/BID raw CSVs are removed from current tracking; local copies remain. Earlier Git history/tags still contain them. Redistribution rights are unverified.
