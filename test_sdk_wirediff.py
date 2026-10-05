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
                with self.assertRaisesRegex(sdk_wirediff.WireDiffError, "stay inside the manifest directory"):
                    sdk_wirediff.compare_manifest(manifest)

    def test_attempts_are_redacted_without_changing_their_shape(self):
        observation = sdk_wirediff.normalize_observation({
            "request": {"url": "https://synthetic.invalid/x?apiKey=A&page_token=P", "headers": {"Authorization ": "B"}},
            "response": {"url": "https://user:F@synthetic.invalid/x?page=2"},
            "attempts": [
                {
                    "url": "https://synthetic.invalid/x?client_secret=C&page=2",
                    "headers": {"X-Goog-Api-Key": "D", "Retry-After": 1},
                    "response": {"headers": {"Set-Cookie": "E"}},
                },
                {"headers": [["Retry-After", "1"]], "query": "page=2", "url": "http://[::1/x"},
            ],
        })
        text = json.dumps(observation)
        for secret in ('"A"', '"B"', "C&", '"D"', '"E"', "F@"):
            self.assertNotIn(secret, text)
        self.assertEqual(observation["request"]["query"]["page_token"], "P")
        first = observation["attempts"][0]
        self.assertEqual(first["url"], "https://synthetic.invalid/x?client_secret=[REDACTED]&page=2")
        self.assertEqual(first["headers"]["Retry-After"], 1)
        self.assertEqual(observation["response"]["url"], "https://synthetic.invalid/x?page=2")
        self.assertEqual(observation["attempts"][1]["query"], "page=2")
        self.assertEqual(observation["attempts"][1]["url"], "[REDACTED]")

    def test_repro_replays_probe_names_with_pointer_characters(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.json"
            path.write_text(json.dumps({
                "adapters": {
                    "typescript": {"inline": {"a": 1}}, "python": {"inline": {"a": 2}}, "go": {"inline": {"a": 1}},
                },
                "compare": {"defaults": {"a/b~c": "/a"}},
            }), encoding="utf-8")
            result = sdk_wirediff.compare_manifest(path)
            path.write_text(json.dumps(sdk_wirediff.minimal_repro(result)), encoding="utf-8")
            replay = sdk_wirediff.compare_manifest(path)
        self.assertEqual(replay["diffs"], result["diffs"])


if __name__ == "__main__":
    unittest.main()
