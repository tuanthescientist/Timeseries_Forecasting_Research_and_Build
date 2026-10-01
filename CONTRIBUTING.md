# Contributing

Use a focused branch and explain the research question or bug addressed. Run:

```bash
python -m unittest discover -s tests -v
python scripts/check_repository.py
ts-benchmark --csv data/demo/synthetic_prices.csv --output results/local/check
```

For a new model, document exactly which information is available at the origin,
how hyperparameters are selected, the training/calibration periods, seeds, dependencies,
and compute requirements. Compare against persistence using identical targets and origins.
Retain per-origin predictions and report negative results.

Do not commit credentials, `.env`, raw provider datasets, model weights, execution
outputs, or personal paths. Clear notebook outputs before committing. Supply upstream
attribution and confirm reuse rights for imported code or data. Historical notebooks
should remain labelled exploratory until their experiments are independently reproduced.
