import json
from pathlib import Path
import tempfile
import unittest

import sdk_wirediff


ROOT = Path(__file__).resolve().parent
DEMO = ROOT / "fixtures" / "demo" / "manifest.json"


class WireDiffTest(unittest.TestCase):
    def test_demo_has_three_stable_explainable_divergences(self):
        first = sdk_wirediff.compare_manifest(DEMO, allow_command=True)
        second = sdk_wirediff.compare_manifest(DEMO, allow_command=True)
        self.assertEqual(sdk_wirediff.canonical_json(first), sdk_wirediff.canonical_json(second))
        self.assertEqual(first["summary"]["divergenceCount"], 3)
        self.assertEqual(first["summary"]["divergentCategories"], ["defaults", "nulls", "retries"])
        self.assertEqual(
            [(item["category"], item["adapter"]) for item in first["diffs"]],
            [("defaults", "go"), ("retries", "python"), ("nulls", "python")],
        )
        report = sdk_wirediff.render_html(first)
        self.assertIn("3</strong><br>divergences", report)
        self.assertNotIn("<script", report.lower())

    def test_command_adapters_are_opt_in(self):
        with self.assertRaisesRegex(sdk_wirediff.WireDiffError, "--allow-command"):
            sdk_wirediff.compare_manifest(DEMO)

    def test_minimal_repro_is_self_contained_and_replays_same_three_diffs(self):
        result = sdk_wirediff.compare_manifest(DEMO, allow_command=True)
        repro = sdk_wirediff.minimal_repro(result)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "repro.json"
            path.write_text(json.dumps(repro), encoding="utf-8")
            replay = sdk_wirediff.compare_manifest(path)
        self.assertEqual(replay["summary"]["divergenceCount"], 3)
        self.assertEqual(replay["summary"]["divergentCategories"], ["defaults", "nulls", "retries"])


if __name__ == "__main__":
    unittest.main()
