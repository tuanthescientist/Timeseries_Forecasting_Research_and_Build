# ADR 0002: training-only volatility terciles

Decision date: 8 October 2026. Status: accepted for foundation v1.

Use trailing 30-day Low-to-Low log-change volatility, with tercile boundaries fitted on
initial training only. Features at each origin use past and current closed observations.
The thresholds remain fixed during validation, calibration and evaluation.

This makes the group definition auditable and avoids defining regimes using favourable
test errors. Sparse high-volatility groups may be inconclusive. Coverage in these groups
is empirical, not universal conditional coverage. Adaptive grouping requires a new amendment.
