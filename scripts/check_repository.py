"""Repository hygiene checks that need no network and no market data.

* notebooks are valid, small, and contain no machine-specific paths in code or outputs;
* Markdown links between repository files resolve;
* no raw market data, credentials or environment files are tracked.
"""

import json
import re
import subprocess
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
MAX_NOTEBOOK_BYTES = 3_000_000
LOCAL_PATH = re.compile(
    r"[A-Za-z]:\\(?:Users|Data Science)\\|/home/[A-Za-z0-9_.-]+/|/Users/[A-Za-z0-9_.-]+/")
FORBIDDEN_TRACKED = re.compile(
    r"(^|/)(\.env(\..*)?|kaggle\.json|.*credentials.*\.json)$|^data/raw/(?!\.gitkeep$)")


def tracked_files():
    try:
        out = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True,
                             check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return None
    return out.splitlines()


def check_notebooks(errors):
    notebooks = sorted((ROOT / "notebooks").glob("*.ipynb"))
    if not notebooks:
        errors.append("No notebooks found")
    for path in notebooks:
        if path.stat().st_size > MAX_NOTEBOOK_BYTES:
            errors.append(f"{path.name}: larger than {MAX_NOTEBOOK_BYTES} bytes")
        nb = json.loads(path.read_text(encoding="utf-8"))
        if nb.get("nbformat") != 4 or not nb.get("cells"):
            errors.append(f"Invalid notebook: {path.name}")
            continue
        for number, cell in enumerate(nb["cells"], 1):
            text = "".join(cell.get("source", []))
            for output in cell.get("outputs", []):
                text += "".join(output.get("text", []))
                text += "".join(output.get("traceback", []))
                text += "".join(output.get("data", {}).get("text/plain", []))
                if output.get("output_type") == "error":
                    errors.append(f"{path.name} cell {number}: saved error output")
            if LOCAL_PATH.search(text):
                errors.append(f"{path.name} cell {number}: machine-specific path")
    return notebooks


def check_links(errors):
    markdown = [ROOT / "README.md", ROOT / "CONTRIBUTING.md"]
    for folder in ("docs", "data", "results"):
        markdown.extend((ROOT / folder).rglob("*.md"))
    documents = [(p, p.read_text(encoding="utf-8")) for p in markdown if p.exists()]
    for path in sorted((ROOT / "notebooks").glob("*.ipynb")):
        for cell in json.loads(path.read_text(encoding="utf-8"))["cells"]:
            if cell["cell_type"] == "markdown":
                documents.append((path, "".join(cell["source"])))
    for path, text in documents:
        for target in re.findall(r"\]\(([^)\s]+)\)", text):
            if target.startswith(("https://", "http://", "mailto:", "#")):
                continue
            target = unquote(target.split("#")[0])
            if target and not (path.parent / target).exists():
                errors.append(f"Broken link in {path.relative_to(ROOT)}: {target}")
    return len(documents)


def check_tracked(errors):
    files = tracked_files()
    if files is None:
        return
    for name in files:
        if FORBIDDEN_TRACKED.search(name):
            errors.append(f"Must not be tracked: {name}")


def main():
    errors = []
    notebooks = check_notebooks(errors)
    documents = check_links(errors)
    check_tracked(errors)
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Checked {len(notebooks)} notebooks and {documents} Markdown documents")


if __name__ == "__main__":
    main()
