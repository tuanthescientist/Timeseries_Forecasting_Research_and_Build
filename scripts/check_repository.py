"""Check published notebook hygiene and internal Markdown links without dependencies."""

import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote


def main():
    root = Path(__file__).resolve().parents[1]
    errors = []
    notebooks = list((root / "notebooks").rglob("*.ipynb"))
    for path in notebooks:
        nb = json.loads(path.read_text(encoding="utf-8"))
        if nb.get("nbformat") != 4 or not nb.get("cells"):
            errors.append(f"Invalid notebook: {path.name}")
        for cell in nb["cells"]:
            if cell["cell_type"] == "code" and (cell.get("outputs") or cell.get("execution_count") is not None):
                errors.append(f"Saved output: {path.name}")
            source = "".join(cell.get("source", []))
            if re.search(r"[A-Za-z]:\\(?:Users|Data Science)\\", source):
                errors.append(f"Machine-specific path: {path.name}")
    markdown = [root / "README.md", root / "CONTRIBUTING.md"]
    for folder in ("docs", "notebooks", "data", "results"):
        markdown.extend((root / folder).rglob("*.md"))
    for path in markdown:
        for target in re.findall(r"\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
            if target.startswith(("https://", "http://", "mailto:", "#")):
                continue
            target = unquote(target.split("#")[0])
            if not (path.parent / target).exists():
                errors.append(f"Broken link in {path.relative_to(root)}: {target}")
    manifest = json.loads((root / "docs/source_manifest.json").read_text(encoding="utf-8"))
    for entry in manifest["files"]:
        path = root / entry["published_path"]
        if hashlib.sha256(path.read_bytes()).hexdigest() != entry["published_sha256"]:
            errors.append(f"Published source hash mismatch: {entry['published_path']}")
    run = json.loads((root / "results/demo/run.json").read_text(encoding="utf-8"))
    for relative, key in (("data/demo/synthetic_prices.csv", "input_sha256"),
                          ("src/tsresearch/benchmark.py", "benchmark_sha256")):
        if hashlib.sha256((root / relative).read_bytes()).hexdigest() != run[key]:
            errors.append(f"Demo artifact hash mismatch: {relative}")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Checked {len(notebooks)} notebooks and {len(markdown)} Markdown files")


if __name__ == "__main__":
    main()
