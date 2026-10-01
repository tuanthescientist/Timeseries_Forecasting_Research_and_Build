# Time-Series Forecasting: Research & Build

**An applied research portfolio on financial forecasting, with an auditable evaluation core.**

Maintained by [Tuan Tran](https://github.com/tuanthescientist).

This project brings together exploratory work on Bitcoin, BNB, the VN30 equity index,
and gold. It examines statistical forecasting, gradient boosting, recurrent neural
networks, and pretrained time-series models. A small reproducible benchmark provides
a common starting point for evaluating those ideas under explicit information constraints.

**Current status:** the NumPy benchmark is runnable and tested; the historical notebooks
are exploratory and have not been revalidated end to end. The published benchmark uses
synthetic data to demonstrate the evaluation pipeline. No real-market performance,
state-of-the-art result, or trading profitability is claimed.

## Research questions

1. Can richer models improve on persistence and drift across forecast horizons?
2. How sensitive are comparisons to forecast origin, regime changes, and target design?
3. Which gains remain when feature construction, preprocessing, and calibration use only
   information available when a forecast is issued?

## Start here

| For reviewers | Evidence |
| --- | --- |
| Understand the research scope | [Research overview](docs/research_overview.md) |
| Read the PhD research proposal | [Research proposal — Tran Anh Tuan (Word)](docs/proposals/PhD_Research_Proposal_Tran_Anh_Tuan.docx) |
| Inspect the evaluation design | [Protocol](docs/evaluation_protocol.md) and [implementation](src/tsresearch/benchmark.py) |
| Reproduce a complete run | [Quick start below](#quick-start) and [demo results](results/demo/README.md) |
| Explore earlier model development | [Notebook catalogue](notebooks/README.md) |
| Check limitations and provenance | [Data card](data/README.md), [audit](docs/research_audit.md), and [source manifest](docs/source_manifest.json) |

## Quick start

Use Python 3.11 or 3.12. Run these commands from the repository root:

```bash
git clone https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build.git
cd Timeseries_Forecasting_Research_and_Build
python -m venv .venv
```

Activate the environment:

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

```bash
# macOS / Linux
source .venv/bin/activate
```

Install and run:

```bash
python -m pip install -c requirements-lock.txt -e .
python -m unittest discover -s tests -v
python scripts/check_repository.py
ts-benchmark --csv data/demo/synthetic_prices.csv --output results/local/demo
```

Each run produces `predictions.csv`, `metrics.csv`, and `run.json` with input and code
hashes, package versions, and evaluation parameters. Compare your metrics with the
[committed demo](results/demo/metrics.csv); allow normal floating-point differences
across platforms. `python scripts/make_demo_data.py` regenerates the synthetic input.

### Evaluate your own series

Place a CSV in `data/raw/`, which is ignored by Git. Supply `ds` (ISO date) and `y`
(strictly positive price), sorted by date with no duplicates. Additional columns are
ignored by the benchmark. Dates are validated; missing sessions are not imputed.

```bash
ts-benchmark --csv data/raw/my_series.csv --horizons 1 7 30 --folds 12 --step 7 --output results/local/my_series
```

The default settings need at least 248 observations. Horizons count **observations**:
30 equity trading sessions and 30 cryptocurrency daily bars represent different periods.
The forecast origin is after the current observation is known; predicting today's low
before today's session closes is a different task.

## What is implemented

| Component | Scope | Status |
| --- | --- | --- |
| Persistence and drift | Reference forecasts at each origin | Tested benchmark |
| Ridge on log returns | Direct horizons; lagged returns and volatility; training-only scaling | Tested benchmark |
| MAE, RMSE, MAPE | Per model and horizon; per-origin predictions retained | Tested benchmark |
| LightGBM / CatBoost | Financial feature and target experiments | Historical notebooks |
| NeuralProphet / AutoARIMA | Decomposable and statistical forecasts | Historical notebooks |
| Recurrent networks | Bitcoin and gold experiments | Historical notebooks |
| Chronos | Pretrained model exploration on Bitcoin | Historical notebook |

Notebook libraries require separate environments. The lightweight installation above
supports the benchmark only; it does not install TensorFlow, PyTorch, or notebook models.

## Repository map

```text
src/tsresearch/          Reusable evaluation core and CLI
tests/                  Temporal integrity, input, and metric checks
notebooks/exploratory/   Selected historical notebooks, cleared outputs
data/demo/              Deterministic synthetic input
data/raw/               Ignored local market data
results/demo/           Reproducible synthetic benchmark artifacts
docs/                   Research scope, protocol, provenance, limitations
scripts/                Synthetic data generator and repository checks
.github/workflows/      Automated core checks on Python 3.11 and 3.12
```

## Next research milestones

- Establish dated market-data snapshots with documented source and usage rights.
- Port selected notebook models into the same evaluation protocol.
- Separate model selection, calibration, and final evaluation periods.
- Extend evaluation across assets and regimes, reporting failed experiments as well as gains.
- Investigate uncertainty calibration and regime robustness once a reliable comparison exists.

These are planned directions, not completed findings. See the
[research overview](docs/research_overview.md) for the proposed experimental sequence.

## Attribution and reuse

The source manifest identifies the local notebook versions used in this portfolio.
Model families and third-party libraries are existing methods; their use here is not a
claim of inventing them. Upstream provenance for historical notebook code is incomplete.
No blanket open-source license is granted in this initial release; see
[attribution and reuse](docs/attribution.md). Market data and model weights are not bundled.

For a research discussion, refer to an exact commit and the relevant protocol or notebook.
