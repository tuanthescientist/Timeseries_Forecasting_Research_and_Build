"""Predeclared comparison utilities; asymptotic tests require optional SciPy."""
from __future__ import annotations

import math
import random
import statistics


def holm(pvalues: list[float]) -> list[float]:
    if any(not 0 <= p <= 1 for p in pvalues):
        raise ValueError("Invalid p-value")
    order = sorted(range(len(pvalues)), key=pvalues.__getitem__)
    adjusted = [0.0] * len(pvalues)
    previous = 0.0
    for rank, index in enumerate(order):
        previous = max(previous, min(1.0, (len(order) - rank) * pvalues[index]))
        adjusted[index] = previous
    return adjusted


def block_bootstrap_mean(values: list[float], block: int = 30,
                         samples: int = 1000, seed: int = 42) -> tuple[float, float]:
    """Circular fixed-block bootstrap, not the stationary bootstrap."""
    if len(values) < 2 * block or block < 1 or samples < 40:
        raise ValueError("Insufficient data or bootstrap samples")
    rng, n = random.Random(seed), len(values)
    estimates = []
    for _ in range(samples):
        sample = []
        while len(sample) < n:
            start = rng.randrange(n)
            sample.extend(values[(start + j) % n] for j in range(block))
        estimates.append(statistics.mean(sample[:n]))
    estimates.sort()
    return estimates[int(0.025 * (samples - 1))], estimates[int(0.975 * (samples - 1))]


def dm_test(differences: list[float], horizon: int) -> dict:
    """Bartlett HAC, Harvey correction, Student-t reference; require enough origins."""
    from scipy.stats import t

    n = len(differences)
    if horizon < 1 or n < max(50, 5 * horizon):
        raise ValueError("Too few matched origins for the declared accuracy test")
    mean = statistics.mean(differences)
    centred = [value - mean for value in differences]
    variance = sum(x * x for x in centred) / n
    for lag in range(1, horizon):
        covariance = sum(centred[i] * centred[i - lag] for i in range(lag, n)) / n
        variance += 2 * (1 - lag / horizon) * covariance
    if variance <= 0:
        raise ValueError("Non-positive HAC variance")
    correction = math.sqrt((n + 1 - 2 * horizon + horizon * (horizon - 1) / n) / n)
    statistic = mean / math.sqrt(variance / n) * correction
    return {"statistic": statistic, "pvalue": float(2 * t.sf(abs(statistic), n - 1)),
            "n": n, "hac_lags": horizon - 1, "assumptions": "asymptotic, dependent losses"}


def coverage_tests(misses: list[int], alpha: float) -> dict:
    """Kupiec and first-order Christoffersen diagnostics; not guarantees under dependence."""
    from scipy.stats import chi2

    if len(misses) < 50 or not 0 < alpha < 1 or any(x not in (0, 1) for x in misses):
        raise ValueError("Invalid coverage series or insufficient outcomes")

    def likelihood(successes, failures, probability):
        value = 0.0
        for count, p in ((successes, probability), (failures, 1 - probability)):
            if count:
                value += count * math.log(p)
        return value

    n, count = len(misses), sum(misses)
    uc = max(0.0, 2 * (likelihood(count, n - count, count / n)
                       - likelihood(count, n - count, alpha)))
    counts = [[0, 0], [0, 0]]
    for a, b in zip(misses, misses[1:], strict=False):
        counts[a][b] += 1
    n00, n01, n10, n11 = counts[0] + counts[1]
    if not (n00 + n01 and n10 + n11):
        return {"kupiec_lr": uc, "kupiec_p": float(chi2.sf(uc, 1)),
                "christoffersen_p": None, "reason": "One transition state is unobserved"}
    pooled = (n01 + n11) / (n - 1)
    separate = likelihood(n01, n00, n01 / (n00 + n01))
    separate += likelihood(n11, n10, n11 / (n10 + n11))
    independent = likelihood(n01 + n11, n00 + n10, pooled)
    independence = max(0.0, 2 * (separate - independent))
    return {"kupiec_lr": uc, "kupiec_p": float(chi2.sf(uc, 1)),
            "christoffersen_lr": independence,
            "christoffersen_p": float(chi2.sf(independence, 1)),
            "conditional_coverage_p": float(chi2.sf(uc + independence, 2))}
