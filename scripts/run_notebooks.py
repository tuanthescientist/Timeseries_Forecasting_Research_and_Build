"""Execute the notebooks top to bottom.

    python scripts/run_notebooks.py                 # smoke test: run, discard results
    python scripts/run_notebooks.py --save          # run and store outputs in the notebooks
    TSR_FORCE_DEMO=1 python scripts/run_notebooks.py   # force the synthetic demo data

Notebooks run with their own folder as working directory and the repository's Python
environment as kernel.
"""

from __future__ import annotations

import argparse
import asyncio
import sys
import time
from pathlib import Path

import nbformat
from nbclient import NotebookClient

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = ROOT / "notebooks"


def run(path: Path, save: bool, timeout: int) -> None:
    notebook = nbformat.read(path, as_version=4)
    client = NotebookClient(notebook, timeout=timeout, kernel_name="python3",
                            resources={"metadata": {"path": str(path.parent)}})
    started = time.time()
    client.execute()
    print(f"ok  {path.name}  ({time.time() - started:.0f}s)", flush=True)
    if save:
        for cell in notebook.cells:
            cell.get("metadata", {}).pop("execution", None)
        nbformat.write(notebook, path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("names", nargs="*", help="notebook file names (default: all)")
    parser.add_argument("--save", action="store_true", help="write outputs into the notebooks")
    parser.add_argument("--timeout", type=int, default=3600, help="seconds per cell")
    args = parser.parse_args()
    paths = ([NOTEBOOKS / name for name in args.names] if args.names
             else sorted(NOTEBOOKS.glob("[0-9][0-9]_*.ipynb")))
    if not paths:
        sys.exit("No notebooks found")
    for path in paths:
        run(path, args.save, args.timeout)


if __name__ == "__main__":
    main()
