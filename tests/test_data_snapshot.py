import csv
import hashlib
import json
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

    def test_published_legacy_market_bytes_preserved(self):
        expected = {"vn30.csv": "1b91f9f2d89a35e15478eac85ff6de6d227458b427ff0e2f27b04c9e8042136e",
                    "bid.csv": "918ad01972453e616a6042da5a897c7137cf943105bb6286fb6dbc21ed7923d4"}
        for name, digest in expected.items():
            snapshot = (ROOT / "legacy/data/raw" / name).read_bytes()
            self.assertEqual(hashlib.sha256(snapshot).hexdigest(), digest)
