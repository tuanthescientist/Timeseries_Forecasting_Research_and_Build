import csv
import json
import runpy
import tempfile
import unittest
from pathlib import Path

from btcforecast.data import COLUMNS, ROOT, read_snapshot, verify_snapshot


class SnapshotTests(unittest.TestCase):
    def test_demo_hash_and_daily_calendar(self):
        rows = verify_snapshot("DEMO")
        self.assertEqual(len(rows), 600)

    def test_original_btc_snapshot_is_explicitly_missing(self):
        manifest = json.loads((ROOT / "data/manifest.json").read_text())
        manifest["datasets"]["BTC"]["status"] = "not_acquired"
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "manifest.json"
            path.write_text(json.dumps(manifest))
            with self.assertRaisesRegex(ValueError, "not locked"):
                verify_snapshot("BTC", path)

    def test_tampered_snapshot_rejected_before_parsing(self):
        manifest = json.loads((ROOT / "data/manifest.json").read_text())
        manifest["datasets"]["DEMO"]["sha256"] = "0" * 64
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "manifest.json"
            path.write_text(json.dumps(manifest))
            with self.assertRaisesRegex(ValueError, "hash"):
                verify_snapshot("DEMO", path)

    def test_calendar_and_ohlc_errors_rejected(self):
        cases = [
            [["2020-01-01", 10, 12, 9, 11, 100], ["2020-01-03", 10, 12, 9, 11, 100]],
            [["2020-01-01", 10, 12, 9, 11, 100], ["2020-01-01", 10, 12, 9, 11, 100]],
            [["2020-01-01", 10, 8, 9, 11, 100]],
            [["2020-01-01", 10, 12, 9, 11, -1]],
        ]
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "bad.csv"
            for rows in cases:
                with self.subTest(rows=rows):
                    with path.open("w", newline="") as stream:
                        writer = csv.writer(stream)
                        writer.writerow(COLUMNS)
                        writer.writerows(rows)
                    with self.assertRaises(ValueError):
                        read_snapshot(path)

    def test_raw_policy_covers_legacy_and_nested_paths(self):
        policy = runpy.run_path(str(ROOT / "scripts/check_repository.py"))["forbidden_raw_path"]
        for name in ["data/raw/btc.csv", "legacy/data/raw/vn30.csv", "other/data/raw/x.csv"]:
            self.assertTrue(policy(name))
        self.assertFalse(policy("legacy/data/raw/.gitkeep"))
        self.assertFalse(policy("data/demo/btc_daily.csv"))
