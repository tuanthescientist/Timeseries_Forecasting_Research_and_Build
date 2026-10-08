"""Check acquisition API wiring without importing yfinance or downloading market data."""
import json
import runpy
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

from btcforecast.data import ROOT


class AcquisitionTests(unittest.TestCase):
    def test_exclusive_end_is_mapped_to_yahoo_end_without_changing_design(self):
        namespace = runpy.run_path(str(ROOT / "scripts/acquire_btc_snapshot.py"))
        main = namespace["main"]
        request = json.loads((ROOT / "configs/btc.json").read_text())
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "configs").mkdir()
            (root / "data").mkdir()
            config_path = root / "configs/btc.json"
            config_path.write_text(json.dumps(request))
            (root / "data/manifest.json").write_text(
                json.dumps({"datasets": {"BTC": {"status": "not_acquired"}}}))
            downloader = Mock(side_effect=RuntimeError("intercepted before download"))
            clock = Mock()
            clock.now.return_value = datetime(2026, 10, 9, tzinfo=timezone.utc)
            with patch.dict(main.__globals__, {"ROOT": root, "datetime": clock}):
                with patch.dict("sys.modules", {"yfinance": SimpleNamespace(download=downloader)}):
                    with self.assertRaisesRegex(RuntimeError, "intercepted"):
                        main()
            args, kwargs = downloader.call_args
            self.assertEqual(args, ("BTC-USD",))
            self.assertEqual(kwargs["end"], "2026-10-08")
            self.assertNotIn("end_exclusive", kwargs)
            self.assertFalse(kwargs["auto_adjust"])
            self.assertFalse((root / request["local_path"]).exists())
            self.assertEqual(json.loads(config_path.read_text()), request)
