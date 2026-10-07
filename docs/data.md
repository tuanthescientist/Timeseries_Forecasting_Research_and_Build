# Data for the three primary projects

The author confirmed on 7 October 2026 that the supplied VN30 and BID CSVs were downloaded from **Investing.com**. The provider pages identify the instruments; this attribution does not establish retrieval time, adjustments, redistribution permission or byte-for-byte correspondence with current live pages.

## GitHub availability

**Neither supplied raw CSV is tracked on main as of 8 October 2026.** The repository contains synthetic demo data and derived supplementary results. Raw files under data/raw/ are ignored by Git. Saved notebook outputs contain illustrative rows and plots.

| Supplied file | Source page | Rows and date range | Relation to saved experiments |
| --- | --- | --- | --- |
| VN_30_Historical_Data_Price_numeric_date_fixed.csv | [Investing.com VN30 history](https://www.investing.com/indices/vn-30-historical-data) | 4,426; 2009-01-05–2026-09-28 | Supplementary snapshot; newer than the 4,408-row NeuralProphet run |
| Bank for Investment and Development Stock Price History.csv | [Investing.com BID history](https://www.investing.com/equities/commercial-bank-investment-develop-historical-data) | 3,153; 2014-01-27–2026-09-24 | Matches bytes embedded in the original BID notebook |

Source confirmation is the author's acquisition statement. The VN30 filename indicates numeric/date processing; it should not be described as an untouched export. Original download time and a complete transformation log are not archived.

## Snapshot identity

**VN30 SHA-256**

    1b91f9f2d89a35e15478eac85ff6de6d227458b427ff0e2f27b04c9e8042136e

**BID SHA-256**

    918ad01972453e616a6042da5a897c7137cf943105bb6286fb6dbc21ed7923d4

The BID hash matches the original notebook's embedded compressed CSV. The public notebook reads an external file. A hash for the exact 4,408-row VN30 snapshot is unavailable; substituting the newer file creates a new experiment rather than reproducing the original score.

| Project | Saved snapshot evidence | Input route |
| --- | --- | --- |
| VN30 / NeuralProphet | 4,408 cleaned rows through 2026-09-04; reindexed to 4,610 weekday rows | Date/Price CSV at data/raw/vn30.csv or VN30_CSV; Kaggle path fallback |
| BTC Low / TensorFlow | Yahoo Finance BTC-USD; 4,397 raw daily rows through 2026-09-30; 4,368 feature-complete rows | Live yfinance download; original bytes/hash not archived |
| BID / scikit-learn | 3,153 rows through 2026-09-24; hash above | OHLCV CSV at data/raw/bid.csv or BID_CSV; Kaggle path fallback |

Kaggle paths describe notebook hosting/input paths, not original vendor attribution. A live download or a different snapshot can change metrics.

## Input formats and calendar issues

**NeuralProphet.** Date uses month/day/year; Price is numeric or contains thousands separators. Invalid rows are removed, dates sorted and final duplicates retained. Weekday reindexing and filling include exchange holidays, so steps are not necessarily exchange sessions.

**TensorFlow.** Yahoo Finance daily Open/High/Low/Close/Volume; Low is the target. FRED CBBTCUSD is renamed Low by the fallback but differs from Yahoo daily low and must be identified as another task.

**ExtraTrees.** Date, Price, Open, High, Low and Vol. use month/day/year dates and K/M/B volume suffixes. Invalid/duplicate dates and non-positive closes are rejected. Missing sessions are not filled. OHLC inconsistencies and a missing September 2026 date require reconciliation.

The newer VN30 file contains weekend labels at 2026-07-04, 2026-07-05, 2026-09-26 and 2026-09-27. Their calendar positions require provider/exchange reconciliation. Current provider pages are not immutable copies of these files.

## Provenance still to complete

| Field | Current evidence |
| --- | --- |
| VN30/BID provider | Investing.com, author-confirmed; source pages above |
| Retrieval timestamp | Not recorded |
| Adjustment and revision policy | Not recorded for these exports |
| Transformation log | Incomplete, including VN30 date processing |
| Calendar and time zone | Require reconciliation |
| Raw-data redistribution permission | Not recorded |
| Original BTC and NeuralProphet snapshot bytes | Not archived |

The code's MIT licence does not establish rights over vendor data. Reproducible research needs acquisition records, transformations, calendar checks and frozen snapshots. See the [supplementary data card](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/docs/supplementary/data.md), [evaluation designs](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/docs/evaluation.md) and [saved primary metrics](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/docs/preliminary_results.md).
