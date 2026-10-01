"""
Lightweight feature engineering utilities for Bitcoin (or any OHLCV/price series).

Designed to work out-of-the-box with a DataFrame shaped like your notebook:
  - time column: 'ds' (datetime)
  - price column: 'y' (e.g., Low or Close)
  - volume column: 'volume' (optional)

Focus: compact, fast, and memory‑friendly feature set to improve forecasting
without heavy libraries. Only depends on pandas and numpy.

Example
-------
>>> import pandas as pd
>>> from btc_features import build_features
>>> # df has columns: ds (datetime), y (price), volume (optional)
>>> X, y, cols = build_features(df, time_col='ds', price_col='y', volume_col='volume',
...                             horizon=1, feature_set='light', target_type='price')
>>> # Fit a lightweight model
>>> from sklearn.ensemble import HistGradientBoostingRegressor
>>> m = HistGradientBoostingRegressor(max_depth=6, learning_rate=0.05)
>>> m.fit(X, y)

Notes
-----
- feature_set='light' keeps features small but effective.
- feature_set='plus' adds a few classical indicators (RSI, MACD, Bollinger).
- All numeric features are downcasted to float32 to save memory.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from typing import Iterable, List, Optional, Tuple


# ------------------------------
# Basic technical computations
# ------------------------------

def _ema(series: pd.Series, span: int) -> pd.Series:
    return series.ewm(span=span, adjust=False, min_periods=span).mean()


def rsi(series: pd.Series, window: int = 14) -> pd.Series:
    diff = series.diff()
    gain = diff.clip(lower=0.0)
    loss = -diff.clip(upper=0.0)
    avg_gain = gain.ewm(alpha=1 / window, adjust=False, min_periods=window).mean()
    avg_loss = loss.ewm(alpha=1 / window, adjust=False, min_periods=window).mean()
    rs = avg_gain / (avg_loss + 1e-12)
    return 100.0 - (100.0 / (1.0 + rs))


def macd(series: pd.Series,
         span_fast: int = 12,
         span_slow: int = 26,
         span_signal: int = 9) -> Tuple[pd.Series, pd.Series, pd.Series]:
    ema_fast = _ema(series, span_fast)
    ema_slow = _ema(series, span_slow)
    macd_line = ema_fast - ema_slow
    signal = macd_line.ewm(span=span_signal, adjust=False, min_periods=span_signal).mean()
    hist = macd_line - signal
    return macd_line, signal, hist


def bollinger(series: pd.Series, window: int = 20, num_std: float = 2.0) -> Tuple[pd.Series, pd.Series, pd.Series, pd.Series]:
    ma = series.rolling(window, min_periods=window).mean()
    std = series.rolling(window, min_periods=window).std()
    upper = ma + num_std * std
    lower = ma - num_std * std
    width = (upper - lower)
    return ma, upper, lower, width


# ------------------------------
# Feature blocks
# ------------------------------

def add_time_features(df: pd.DataFrame, time_col: str = 'ds') -> pd.DataFrame:
    out = df.copy()
    if not np.issubdtype(out[time_col].dtype, np.datetime64):
        out[time_col] = pd.to_datetime(out[time_col], errors='coerce')

    # Day-of-week and month cyclic encodings keep dimensionality low
    dow = out[time_col].dt.dayofweek.astype('float32')  # 0-6
    month = out[time_col].dt.month.astype('float32')    # 1-12
    out['dow_sin'] = np.sin(2 * np.pi * dow / 7.0)
    out['dow_cos'] = np.cos(2 * np.pi * dow / 7.0)
    out['mon_sin'] = np.sin(2 * np.pi * (month - 1.0) / 12.0)
    out['mon_cos'] = np.cos(2 * np.pi * (month - 1.0) / 12.0)

    # Month boundaries can matter for crypto flows
    out['is_month_start'] = (out[time_col].dt.is_month_start).astype('int8')
    out['is_month_end'] = (out[time_col].dt.is_month_end).astype('int8')
    return out


def add_return_and_lags(df: pd.DataFrame,
                        price_col: str = 'y',
                        lag_steps: Iterable[int] = (1, 3, 7),
                        ret_steps: Iterable[int] = (1, 3, 7, 14)) -> pd.DataFrame:
    out = df.copy()
    logp = np.log(out[price_col].astype('float64'))
    for k in ret_steps:
        out[f'ret_{k}'] = logp.diff(k)
    for k in lag_steps:
        out[f'lag_{price_col}_{k}'] = out[price_col].shift(k)
    return out


def add_rolling_stats(df: pd.DataFrame,
                      price_col: str = 'y',
                      windows: Iterable[int] = (7, 14, 21)) -> pd.DataFrame:
    out = df.copy()
    log_ret_1 = np.log(out[price_col]).diff()
    for w in windows:
        out[f'vol_{w}'] = log_ret_1.rolling(w, min_periods=w).std() * np.sqrt(w)
        ma = out[price_col].rolling(w, min_periods=w).mean()
        out[f'mom_ma_{w}'] = out[price_col] / ma - 1.0
        roll_max = out[price_col].rolling(w, min_periods=w).max()
        roll_min = out[price_col].rolling(w, min_periods=w).min()
        out[f'dist_high_{w}'] = out[price_col] / roll_max - 1.0
        out[f'dist_low_{w}'] = out[price_col] / roll_min - 1.0
    # One compact EMA ratio feature
    out['ema_ratio_7_21'] = _ema(out[price_col], 7) / (_ema(out[price_col], 21) + 1e-12) - 1.0
    return out


def add_volume_features(df: pd.DataFrame,
                        volume_col: Optional[str] = 'volume',
                        windows: Iterable[int] = (7, 14)) -> pd.DataFrame:
    out = df.copy()
    if volume_col is None or volume_col not in out.columns:
        return out
    lv = np.log(out[volume_col].replace(0, np.nan))
    out['log_vol'] = lv
    out['dlog_vol_1'] = lv.diff(1)
    for w in windows:
        mean = lv.rolling(w, min_periods=w).mean()
        std = lv.rolling(w, min_periods=w).std()
        out[f'vol_z_{w}'] = (lv - mean) / (std + 1e-12)
    return out


def add_plus_indicators(df: pd.DataFrame, price_col: str = 'y') -> pd.DataFrame:
    out = df.copy()
    out['rsi_14'] = rsi(out[price_col], 14)
    macd_line, signal, hist = macd(out[price_col])
    out['macd'] = macd_line
    out['macd_signal'] = signal
    out['macd_hist'] = hist
    ma, upper, lower, width = bollinger(out[price_col])
    out['bb_width_20'] = width / (ma + 1e-12)
    out['bb_perc_20'] = (out[price_col] - lower) / (width + 1e-12)
    return out


# ------------------------------
# Orchestrator
# ------------------------------

def build_features(df: pd.DataFrame,
                   time_col: str = 'ds',
                   price_col: str = 'y',
                   volume_col: Optional[str] = 'volume',
                   horizon: int = 1,
                   feature_set: str = 'light',  # 'light' | 'plus'
                   target_type: str = 'price',  # 'price' | 'return'
                   dropna: bool = True) -> Tuple[pd.DataFrame, pd.Series, List[str]]:
    """
    Generate a compact feature matrix X, target y, and list of feature names.

    Params
    ------
    df : DataFrame with at least [time_col, price_col]. volume_col is optional.
    horizon : forecast steps ahead (e.g., 1 for next period).
    feature_set : 'light' (fast, small) or 'plus' (adds RSI, MACD, BB).
    target_type : 'price' (predict future price) or 'return' (log-return).
    dropna : drop rows with NaNs after feature assembly and target shift.

    Returns
    -------
    X : pd.DataFrame of features (float32)
    y : pd.Series target aligned to X index (float32)
    feature_cols : list[str]
    """
    if df.empty:
        raise ValueError("Input DataFrame is empty")

    work = df.copy()
    # Ensure time sorted for rolling/shift correctness
    if time_col in work.columns:
        work = work.sort_values(time_col).reset_index(drop=True)

    # Core blocks
    work = add_time_features(work, time_col=time_col)
    work = add_return_and_lags(work, price_col=price_col)
    work = add_rolling_stats(work, price_col=price_col)
    work = add_volume_features(work, volume_col=volume_col)

    if feature_set.lower() == 'plus':
        work = add_plus_indicators(work, price_col=price_col)

    # Assemble feature columns (exclude raw and time)
    exclude = {time_col, price_col}
    feature_cols = [c for c in work.columns if c not in exclude]

    # Target construction
    if target_type == 'price':
        y = work[price_col].shift(-horizon)
    elif target_type == 'return':
        y = np.log(work[price_col]).shift(-horizon) - np.log(work[price_col])
    else:
        raise ValueError("target_type must be 'price' or 'return'")

    # Replace infs and optionally drop NaNs introduced by rolling/shift
    work[feature_cols] = work[feature_cols].replace([np.inf, -np.inf], np.nan)
    y = y.replace([np.inf, -np.inf], np.nan)

    if dropna:
        mask = work[feature_cols].notna().all(axis=1) & y.notna()
        work = work.loc[mask]
        y = y.loc[mask]

    # Downcast to float32 for compactness
    X = work[feature_cols].astype('float32')
    y = y.astype('float32')

    return X, y, feature_cols


def time_series_train_test_split(
    X: pd.DataFrame,
    y: pd.Series,
    test_size: float = 0.2
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Simple chronological split without shuffling.
    """
    n = len(X)
    if n == 0:
        raise ValueError("Empty X")
    k = int(n * (1 - test_size))
    return X.iloc[:k], X.iloc[k:], y.iloc[:k], y.iloc[k:]


# Convenience: quick baseline model that stays light and fast
def train_light_baseline(X: pd.DataFrame, y: pd.Series):
    """
    Train a compact baseline regressor (sklearn's HistGradientBoostingRegressor).
    Returns the fitted model. Use for quick benchmarking.
    """
    from sklearn.ensemble import HistGradientBoostingRegressor

    model = HistGradientBoostingRegressor(
        max_depth=6,
        learning_rate=0.05,
        max_bins=64,
        l2_regularization=0.0,
        random_state=42
    )
    model.fit(X, y)
    return model
