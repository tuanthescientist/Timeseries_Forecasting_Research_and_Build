"""Shared test helpers (``unittest discover -s tests`` puts this folder on ``sys.path``)."""

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load_generator():
    spec = importlib.util.spec_from_file_location(
        "make_demo_ohlcv", ROOT / "scripts" / "make_demo_ohlcv.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


make_ohlcv = _load_generator().make_ohlcv
