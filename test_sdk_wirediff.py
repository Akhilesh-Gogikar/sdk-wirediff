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
        self.assertIn('href="#main-content"', report)
        self.assertIn('<caption>Baseline-relative semantic differences</caption>', report)
        self.assertIn('th scope="col"', report)

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
        for adapter in repro["adapters"].values():
            self.assertEqual(sorted(adapter["inline"]["semantics"]), ["defaults", "nulls", "retries"])

    def test_observation_paths_cannot_leave_the_manifest_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            outside = root / "outside.json"
            outside.write_text('{"secret": "LOCAL-FILE-CONTENT"}', encoding="utf-8")
            (root / "fixture").mkdir()
            inline = {"inline": {}}
            for escape in ("../outside.json", str(outside)):
                manifest = root / "fixture" / "manifest.json"
                manifest.write_text(json.dumps({
                    "adapters": {"typescript": {"observation": escape}, "python": inline, "go": inline},
                    "compare": {},
                }), encoding="utf-8")
                with self.assertRaisesRegex(sdk_wirediff.WireDiffError, "inside the manifest directory"):
                    sdk_wirediff.compare_manifest(manifest)

    def test_attempt_headers_and_queries_are_redacted(self):
        observation = sdk_wirediff.normalize_observation({
            "request": {"url": "https://synthetic.invalid/x?apiKey=A&page_token=P", "headers": {"Authorization ": "B"}},
            "attempts": [{
                "url": "https://synthetic.invalid/x?client_secret=C",
                "headers": {"X-Goog-Api-Key": "D", "Idempotency-Key": "kept"},
                "response": {"headers": {"Set-Cookie": "E"}},
            }],
        })
        text = json.dumps(observation)
        for secret in ('"A"', '"B"', '"C"', '"D"', '"E"', "synthetic.invalid"):
            self.assertNotIn(secret, text)
        self.assertEqual(observation["request"]["query"]["page_token"], "P")
        self.assertEqual(observation["attempts"][0]["headers"]["idempotency-key"], "kept")


if __name__ == "__main__":
    unittest.main()
