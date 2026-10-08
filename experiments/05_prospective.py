"""Validate eligibility only; never manufacture a prospective result."""
from btcforecast.protocol import require_prospective

if __name__ == "__main__":
    require_prospective()
    raise SystemExit(
        "Eligibility checked. A separately frozen forecast export and prospective acquisition "
        "manifest are still required; this script does not execute a prospective experiment."
    )
