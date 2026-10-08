import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from btcforecast.protocol import ROOT, fingerprint, load_protocol, require_prospective


class ProtocolTests(unittest.TestCase):
    def test_canonical_hash_ignores_json_key_order(self):
        self.assertEqual(fingerprint({"a": 1, "b": 2}), fingerprint({"b": 2, "a": 1}))
        self.assertNotEqual(fingerprint({"a": 1}), fingerprint({"a": 2}))

    def test_current_protocol_has_four_horizons(self):
        config, digest = load_protocol()
        self.assertEqual(config["horizons"], [1, 5, 20, 30])
        self.assertEqual(len(digest), 64)

    def test_changed_config_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "configs").mkdir()
            config = json.loads((ROOT / "configs/protocol.json").read_text())
            config["horizons"] = [1]
            (root / "configs/protocol.json").write_text(json.dumps(config))
            (root / "configs/protocol-lock.json").write_bytes(
                (ROOT / "configs/protocol-lock.json").read_bytes())
            with self.assertRaisesRegex(ValueError, "differs"):
                load_protocol(root)

    def test_prospective_cannot_run_without_completion_record(self):
        with patch("btcforecast.protocol._git") as mocked:
            mocked.side_effect = lambda root, *args: (ROOT / args[1].split(":", 1)[1]).read_bytes()
            with self.assertRaisesRegex(ValueError, "not completed"):
                require_prospective()

    def test_lock_is_design_only_until_btc_snapshot_is_acquired(self):
        lock = json.loads((ROOT / "configs/protocol-lock.json").read_text())
        self.assertEqual(lock["scope"], "foundation_design_only")
        self.assertEqual(lock["base_commit"], "eb1eac0d4fc70e42eba3be0aa07b5b24198d8c63")

    def test_foundation_tag_cannot_be_promoted_by_a_completion_marker(self):
        import shutil

        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            lock = json.loads((ROOT / "configs/protocol-lock.json").read_text())
            for name in ["configs/protocol.json", "configs/protocol-lock.json", *lock["artifacts"]]:
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / name, target)
            completion = root / "results/tables/retrospective_completion.json"
            completion.parent.mkdir(parents=True)
            completion.write_text("{}")
            with patch("btcforecast.protocol._git") as mocked:
                mocked.side_effect = lambda root, *args: (
                    root / args[1].split(":", 1)[1]).read_bytes()
                with self.assertRaisesRegex(ValueError, "Foundation-only"):
                    require_prospective(root)
