# Contributing

Use a focused branch and say which research question or defect it addresses.

```bash
python -m pip install -c requirements-lock.txt -e ".[dev]"
ruff check .
python -m unittest discover -s tests -v
python scripts/check_repository.py
TSR_FORCE_DEMO=1 python scripts/run_notebooks.py   # optional: notebooks on synthetic data
```

Rules that keep results comparable:

* A new model implements the interface in `src/tsresearch/models.py` and is compared with
  persistence on identical origins; hyper-parameters are chosen on the validation segment
  only, and the test segment is run once with frozen choices.
* State exactly what information is available at the forecast origin. Add a test that
  forecasts do not change when data after the origin is altered.
* Report negative results and keep per-origin predictions reproducible.
* Never commit credentials, `.env`, raw provider data (`data/raw/` is ignored), model
  weights, or personal paths. `scripts/check_repository.py` enforces part of this.
* Confirm reuse rights for imported code or data and give attribution.
