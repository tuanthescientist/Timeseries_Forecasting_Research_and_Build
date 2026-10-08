# Registration status and amendment record

Author: Trần Anh Tuấn. Design date: 8 October 2026.
Base evidence commit: eb1eac0d4fc70e42eba3be0aa07b5b24198d8c63.
Foundation tag: protocol-v1, to be published with the reviewed branch commit.
Resolve the exact tagged commit through git rev-parse protocol-v1^{commit}; the
hash is not embedded into its own commit. Artifact hashes are in
[protocol-lock.json](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/research/btc-interval-calibration/configs/protocol-lock.json).

## What is being frozen

The BTC Low target, four horizons, chronological stages, baseline definitions,
temporal feedback rules, training-only groups, foundation interval settings and
primary comparison family in [protocol.md](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/research/btc-interval-calibration/docs/protocol.md) are design decisions.

The lock's scope is foundation_design_only. Original history and its notebook metrics
have already been inspected. The retrospective evaluation is not an untouched
prospective test. A Git tag demonstrates the date of this design record, not an external
registration or evidence that all implementation/selection decisions preceded outcomes.

## Outstanding conditions

No new BTC snapshot is locked. Exact attention features/settings, EnbPI and the proposed
method remain pending. No retrospective completion record or prospective predictions exist.
The tag does not imply a completed preregistration for the whole model study.

Before additional model comparisons, publish a versioned amendment specifying the remaining
decisions and acquisition hash. Before prospective data collection, commit the frozen A–D
artifacts and confirm a future start. The candidate window is 2026-10-09–2027-04-06; if those
conditions are not met before its start, replace it with a new future window in an amendment.

## Evidence required for prospective evaluation

A completion record must name stages A, B, C and D, the protocol hash, a valid freeze
commit, and the SHA-256 of every required final artifact. Each artifact must be present
in that commit, with matching local bytes. The freeze must precede the candidate start.
Acquisition and forecast provenance must remain separate from design metadata.

No completion record is created in this change. The prospective driver refuses to
proceed while these conditions are missing.
