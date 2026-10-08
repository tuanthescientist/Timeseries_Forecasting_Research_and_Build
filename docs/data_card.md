# BTC snapshot and provenance

New Yahoo BTC-USD snapshot: acquired 2026-10-08 09:28:01 UTC using yfinance 1.1.0; 4,404 dates, 2014-09-17 through 2026-10-07. SHA-256 e17858686ed88e2d8ac4a02aabb2ea5eec250062d68e78cfc8105b46e9381110. Daily calendar and OHLC constraints passed. [Manifest](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/data/manifest.json). This is a new snapshot, not the original notebook download. Daily Low is not an executable trading price.

Settings: daily interval; auto_adjust=False; repair=False; start 2014-09-17; exclusive end 2026-10-08. Vendor revisions and UTC session alignment remain limitations. Raw CSVs stay local. Fresh checkouts may use python scripts/acquire_btc_snapshot.py --restore with acquisition dependencies: exact hash match is mandatory; revised history requires a new snapshot/amendment. A public hash does not make raw bytes available or ensure long-term reproducibility.

Synthetic demo supports CI only. VN30/BID originated from Investing.com; their CSVs are removed from current tracking, retained locally, and still present in earlier Git history/tags. Redistribution rights remain unverified; no dataset licence is inferred from the software licence.
