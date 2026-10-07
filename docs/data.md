# Data for the three primary projects

Raw market CSVs, downloaded histories and model weights are not distributed in this repository. Saved notebook outputs include illustrative historical rows and figures. Data rights, adjustment policy and source provenance need completion before claiming full reproducibility.

| Project | Saved snapshot evidence | How to supply data |
| --- | --- | --- |
| VN30 / NeuralProphet | 4,408 cleaned source rows; 2009-01-05–2026-09-04; then 4,610 weekday rows with filled gaps | Original Date/Price CSV at data/raw/vn30.csv or environment variable VN30_CSV. Kaggle dataset path is a fallback. |
| BTC Low / TensorFlow | Yahoo Finance BTC-USD daily OHLCV; 4,397 raw rows through 2026-09-30; 4,368 rows after features | Live yfinance download beginning 2014-08-01 and ending at the current date. An exact archived download/hash is not available in the repository. |
| BID / scikit-learn | 3,153 rows; 2014-01-27–2026-09-24; original-byte SHA-256 below | Original OHLCV export at data/raw/bid.csv or environment variable BID_CSV. Kaggle dataset path is a fallback. |

BID original-byte SHA-256:

```text
918ad01972453e616a6042da5a897c7137cf943105bb6286fb6dbc21ed7923d4
```

This hash was verified from the source notebook's embedded compressed CSV. The publication copy removes that raw-data payload and reads an externally supplied CSV; the modeling calculations are unchanged. The source notebook in the user's workspace is preserved.

## Input formats

**NeuralProphet.** Date in month/day/year format and Price as a numeric value or a string with thousands separators. The loader keeps positive, parseable prices, drops invalid rows, sorts dates and keeps the final duplicate. It then uses frequency B and forward/backward filling. A weekday grid includes exchange holidays; it is not an exchange session calendar.

**TensorFlow.** Yahoo Finance Open/High/Low/Close/Volume with a daily timestamp index. Low is the target. The fallback FRED series CBBTCUSD is renamed Low by the notebook but represents a different observation, not Yahoo daily low; results from that fallback must be identified as a different task. The download is not frozen and can be revised by the source.

**ExtraTrees.** Date, Price, Open, High, Low and Vol. with month/day/year dates, thousands separators and K/M/B volume suffixes. Duplicate or invalid dates and non-positive closing prices are rejected. Missing sessions are not filled. The notebook flags OHLC inconsistencies and a missing September 2026 date; check them against a documented provider before using the result as final research evidence.

## Provenance still to complete

The VN30 and BID notebook paths identify a Kaggle-hosted dataset, not an original financial vendor or redistribution licence. Their original provider, retrieval record, price adjustment policy and redistribution rights are not verified. A hash of the exact 4,408-row VN30 snapshot is not available; the newer local file should not be substituted silently for it. For Bitcoin, the code names Yahoo Finance via yfinance, but the exact saved download bytes and data-use terms are not archived here.

The code's MIT licence does not grant rights to third-party market data. Local raw files are ignored by Git. Reproducing with a different snapshot is a new run and should be documented with a date, hash and updated scores.

## Separate supplementary snapshots

The supplemental VN30 benchmark uses **4,426** source rows through 28 September 2026, which differs from the NeuralProphet run. Its BID file matches the hash above but its forecasting protocol differs from the primary ExtraTrees project. Details and known issues are in the [supplementary data card](supplementary/data.md). The synthetic OHLCV file under data/demo/ supports only supplementary execution.
