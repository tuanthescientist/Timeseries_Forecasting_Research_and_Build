# Research audit of the initial portfolio

This audit is based on source inspection and tests of the new benchmark. It is not an
end-to-end reproduction of every historical experiment.

| Finding | Treatment in this release |
| --- | --- |
| Numerous notebook copies and forks with overlapping purposes | Nine representative versions selected; source filenames and hashes recorded |
| Saved outputs lack a shared, verified evaluation protocol | Outputs cleared; no historical accuracy leaderboard published |
| Local `test_vn30_mape.py` scales predictions using the mean of test labels | Script excluded from the curated release; such a correction is not a valid prospective test result |
| That script also starts recursive prediction from the last training feature row | Not promoted as a validated forecasting implementation |
| Historical gold notebook contains test-period calibration and alternative adjustments | Kept as exploration; corrected metrics must not be treated as untouched holdout scores |
| Original feature helper accepts arbitrary extra input columns | Kept with historical notebooks only; caller must establish feature availability |
| Absolute VN30 paths and local caches | Exported copies use relative paths under ignored `data/raw/` |
| One upgraded fork is not valid JSON; one training script is empty | Excluded; original files retained locally |
| Market snapshots lack sufficient provenance and redistribution records | Not bundled in the public release |
| Unrelated TypeScript game files, environments, logs, model artifacts, and `.env` | Excluded from the publication directory |

The new core uses an explicit `ds,y` input and direct supervised horizons, enforces
label availability at every origin, and tests invariance to changes after the origin.
These checks improve the integrity of this core; they do not certify the historical
notebooks. Inspection can miss issues, so the notebook catalogue clearly identifies
their unverified status.
