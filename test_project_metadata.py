import pathlib
import unittest

import sdk_wirediff


ROOT = pathlib.Path(__file__).resolve().parent
REQUIRED = [
    "LICENSE", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "SECURITY.md", "SUPPORT.md",
    "GOVERNANCE.md", "ROADMAP.md", "CHANGELOG.md", "ECOSYSTEM.md",
    "docs/ARCHITECTURE.md", "docs/TROUBLESHOOTING.md", "docs/API_STABILITY.md",
    "docs/PRIVACY.md", "docs/ACCESSIBILITY.md", "docs/LAUNCH_KIT.md", "docs/ISSUE_SEEDS.md", ".github/workflows/ci.yml",
    ".github/workflows/release.yml", ".github/dependabot.yml",
    ".github/CODEOWNERS",
    ".github/ISSUE_TEMPLATE/bug.yml", ".github/ISSUE_TEMPLATE/feature.yml",
    ".github/ISSUE_TEMPLATE/config.yml", ".github/pull_request_template.md",
]


class ProjectMetadataTest(unittest.TestCase):
    def test_release_and_community_metadata_is_consistent(self):
        for relative in REQUIRED:
            self.assertTrue((ROOT / relative).exists(), f"missing {relative}")
        metadata = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
        self.assertIn('version = "0.1.0"', metadata)
        self.assertIn('requires-python = ">=3.10,<3.15"', metadata)
        self.assertIn('license = "MIT"', metadata)
        self.assertIn('license-files = ["LICENSE"]', metadata)
        self.assertIn("dependencies = []", metadata)
        self.assertIn('sdk-wirediff = "sdk_wirediff:cli"', metadata)
        for version in ("3.10", "3.11", "3.12", "3.13", "3.14"):
            self.assertIn(f'Programming Language :: Python :: {version}', metadata)
        self.assertEqual(sdk_wirediff.VERSION, "0.1.0")
        license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("Copyright (c) 2026 Akhilesh Gogikar", license_text)
        self.assertEqual((ROOT / ".github/CODEOWNERS").read_text(encoding="utf-8"), "* @Akhilesh-Gogikar\n")
        release = (ROOT / ".github/workflows/release.yml").read_text(encoding="utf-8")
        self.assertIn("gh release create", release)
        self.assertNotRegex(release, r"pip publish|twine|npm publish")


if __name__ == "__main__":
    unittest.main()
