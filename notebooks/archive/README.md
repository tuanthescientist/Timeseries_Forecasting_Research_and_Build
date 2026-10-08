# Original BTC notebook

[btc-low-forecast-tensorflow.ipynb](https://github.com/tuanthescientist/Timeseries_Forecasting_Research_and_Build/blob/main/notebooks/archive/btc-low-forecast-tensorflow.ipynb)
is preserved byte-for-byte from commit eb1eac0. It contains saved historical output and
live-download/training cells. Active CI does not execute it.

The 3.40% saved MAPE evaluates 30 rolling one-step predictions using realised prior days.
It does not score the separate recursive future path. Training callbacks monitor training
loss; the saved run has no separate validation segment. The new protocol addresses these
limitations explicitly.

This notebook is preparation, not evidence that the new four-horizon benchmark or
interval calibration has already been evaluated.
