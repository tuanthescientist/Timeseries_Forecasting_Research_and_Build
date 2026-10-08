# Synthetic daily OHLCV

btc_daily.csv contains 600 deterministic daily rows beginning 2020-01-01.
An oscillating positive price path with deterministic changing amplitude supplies
consistent synthetic Open/High/Low/Close/Volume bars. Its SHA-256 and row count are in
data/manifest.json. It is not an anonymised or transformed market dataset.

The demo driver uses training through index 199, calibration from index 250, evaluation
from index 399, and targets through the final row. These indices exercise delayed
feedback and warm-start separation; they do not replace the research calendar dates.
