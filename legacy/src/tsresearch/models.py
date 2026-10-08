"""Forecasters of multi-horizon log returns.

Every model maps a causal feature row to a vector of h-step log-return forecasts, one per
horizon. ``naive`` predicts zero return (persistence of the last price) and ``drift``
extrapolates the trailing mean return. Learned models are fitted on rows whose longest
label is already observed at the refit origin; see :mod:`tsresearch.backtest`.
"""

from __future__ import annotations

import numpy as np
from sklearn.ensemble import ExtraTreesRegressor, HistGradientBoostingRegressor
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

SEED = 42


class Naive:
    """Persistence of the last price: zero expected log return."""

    def __init__(self, horizons, columns):
        self.n_out = len(horizons)

    def fit(self, X, Y, sample_weight=None):
        return self

    def predict(self, X):
        return np.zeros((len(X), self.n_out))


class Drift:
    """Trailing mean one-step return (``drift_252`` feature) times the horizon."""

    def __init__(self, horizons, columns):
        self.h = np.asarray(horizons, dtype=float)
        self.col = list(columns).index("drift_252")

    def fit(self, X, Y, sample_weight=None):
        return self

    def predict(self, X):
        return np.outer(X[:, self.col], self.h)


class RidgeReturns:
    def __init__(self, horizons, columns, alpha=100.0):
        self.model = make_pipeline(StandardScaler(), Ridge(alpha=alpha))

    def fit(self, X, Y, sample_weight=None):
        self.model.fit(X, Y)
        return self

    def predict(self, X):
        return self.model.predict(X)


class ExtraTrees:
    """One multi-output forest; targets are divided by sqrt(h) so horizons weigh equally."""

    def __init__(self, horizons, columns, min_leaf=40, n_estimators=150, max_depth=8,
                 max_features=0.5):
        self.scale = np.sqrt(np.asarray(horizons, dtype=float))
        self.model = ExtraTreesRegressor(
            n_estimators=n_estimators, max_depth=max_depth, min_samples_leaf=min_leaf,
            max_features=max_features, bootstrap=False, random_state=SEED, n_jobs=-1)

    def fit(self, X, Y, sample_weight=None):
        self.model.fit(X, Y / self.scale)
        return self

    def predict(self, X):
        return self.model.predict(X) * self.scale


class GradientBoosting:
    """Shallow histogram gradient boosting, one regressor per horizon."""

    def __init__(self, horizons, columns, max_depth=3, learning_rate=0.03, max_iter=120,
                 min_leaf=40):
        self.params = dict(max_depth=max_depth, learning_rate=learning_rate, max_iter=max_iter,
                           min_samples_leaf=min_leaf, l2_regularization=1.0,
                           early_stopping=False, random_state=SEED)
        self.models = [HistGradientBoostingRegressor(**self.params) for _ in horizons]

    def fit(self, X, Y, sample_weight=None):
        for j, model in enumerate(self.models):
            model.fit(X, Y[:, j])
        return self

    def predict(self, X):
        return np.column_stack([m.predict(X) for m in self.models])


FAMILIES = {"naive": Naive, "drift": Drift, "ridge": RidgeReturns, "extra_trees": ExtraTrees,
            "gradient_boosting": GradientBoosting}


def make_model(spec: dict, horizons, columns):
    """Build a model from ``{"family": ..., **hyper-parameters}``."""
    params = {k: v for k, v in spec.items() if k != "family"}
    return FAMILIES[spec["family"]](horizons, columns, **params)


def spec_name(spec: dict) -> str:
    """Compact deterministic label, e.g. ``ridge(alpha=100)``."""
    params = ", ".join(f"{k}={v}" for k, v in sorted(spec.items()) if k != "family")
    return f"{spec['family']}({params})" if params else spec["family"]
