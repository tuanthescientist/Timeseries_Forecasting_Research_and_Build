# Contributing

Use a branch and a reviewed pull request. The active project is BTC-USD daily Low.
Legacy portfolio assets must remain identifiable and must not be pooled with new results.

Run unit tests, repository checks and synthetic smoke checks before changing foundations.
CI must not download market data or train the archived attention model.

Data acquisition is explicit. Record SHA-256, retrieval timestamp, requested dates,
provider settings and any transformation. Never overwrite a locked snapshot silently.

The foundation lock covers configs, temporal rules and core code. A change to these
artifacts requires a versioned design amendment, a regenerated lock and a new tag.
Do not describe an amendment made after seeing outcomes as an earlier preregistration.

Actual result tables require complete per-origin forecasts, run metadata, data/protocol
hashes, commit and failures. Synthetic output never constitutes financial accuracy evidence.
