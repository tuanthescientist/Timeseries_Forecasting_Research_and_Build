"""Model candidates and the validation-only rule that chooses among them."""

from __future__ import annotations

import pandas as pd

from .metrics import best_per_family
from .models import spec_name

CANDIDATE_SPECS: list[dict] = (
    [{"family": "naive"}, {"family": "drift"}]
    + [{"family": "ridge", "alpha": alpha} for alpha in (10.0, 100.0, 1000.0)]
    + [{"family": "extra_trees", "min_leaf": leaf} for leaf in (20, 60)]
    + [{"family": "gradient_boosting", "max_depth": depth} for depth in (2, 3)]
)

LEARNED_FAMILIES = ("ridge", "extra_trees", "gradient_boosting")


def choose_models(validation_table: pd.DataFrame, specs: list[dict] | None = None) -> dict:
    """Apply the selection rule to a *validation* ``point_metrics`` table.

    Score = mean over horizons of RMSE relative to persistence (lower is better).
    Returns the best spec of each family (``frozen``), the best learned model, and the
    overall best candidate (``center``), which may be persistence itself.
    """
    specs = specs or CANDIDATE_SPECS
    by_name = {spec_name(s): s for s in specs}
    ranking = best_per_family(validation_table, specs)
    ordered = ranking.sort_values(["mean_rel_rmse", "model"]).reset_index(drop=True)
    frozen = []
    for _, group in ranking.groupby("family", sort=False):
        frozen.append(by_name[group.sort_values(["mean_rel_rmse", "model"]).iloc[0]["model"]])
    learned = ordered[ordered["family"].isin(LEARNED_FAMILIES)]
    return {"ranking": ordered, "frozen": frozen,
            "best_learned": by_name[learned.iloc[0]["model"]],
            "center": by_name[ordered.iloc[0]["model"]]}
