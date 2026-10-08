# BTC-USD daily-Low data card

**New snapshot status: not acquired.** [manifest.json](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/research/btc-interval-calibration/data/manifest.json)
has null BTC retrieval time, hash and row count. These fields must come from an actual
acquisition and validation; they are not inferred from the notebook's metrics.

## Acquisition request

[Yahoo Finance BTC-USD history](https://finance.yahoo.com/quote/BTC-USD/history/),
accessed explicitly through yfinance, is the proposed source. Request daily OHLCV from
2014-09-17 to 2026-10-08 exclusive, auto_adjust=false and repair=false. Preserve package
version and retrieval UTC timestamp. The normalised CSV has date,open,high,low,close,volume.

Require strictly ordered unique ISO UTC dates, one observation per calendar day, positive
finite OHLC, consistent high/low bounds and non-negative volume. Missing observations
cause validation failure and require a documented acquisition amendment; they are not
silently forward-filled. A provider revision creates a different snapshot.

The original notebook requested history from 2014-08-01 and downloaded through its run
date. Its saved output reports 4,397 daily rows through 2026-09-30, with 4,368
feature-complete rows. Original downloaded bytes and SHA-256 are unavailable. New Yahoo
bytes are not represented as a recovery of those historical bytes.

## Target and interpretation

Low is the minimum reported price during the provider's daily bar. Prediction of that
endpoint does not mean the low is available as an executable trading price. Low-to-Low
changes define the foundation's volatility proxy. Close-based tasks need a separately
declared experiment. The FRED fallback in the original notebook is a different target
and is excluded from the new protocol.

The provider's session convention must be checked during acquisition. An ordered
calendar validates timestamps and continuity; it does not independently prove how the
vendor constructed its bars. Adjustment, licensing and vendor revisions remain documented
limitations. Raw BTC data are local; the public manifest records their identity.

## Demonstration and historical assets

data/demo/btc_daily.csv contains 600 deterministic synthetic OHLCV observations. It is
the only dataset used by active CI. Demo split indices are explicitly different from
research dates, and synthetic results are not market evidence.

The two published Investing.com CSVs remain available as historical assets:
[VN30](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/research/btc-interval-calibration/legacy/data/raw/vn30.csv) and [BID](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/research/btc-interval-calibration/legacy/data/raw/bid.csv).
Their bytes and SHA-256 are preserved. They do not enter the BTC protocol.
