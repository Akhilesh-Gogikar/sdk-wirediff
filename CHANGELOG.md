# Changelog

All notable changes are recorded here. The project follows semantic versioning while pre-1.0 compatibility remains intentionally limited; see [API_STABILITY.md](docs/API_STABILITY.md).

## [Unreleased]

## [0.1.1] - 2026-10-05

### Security

- Reject captured-observation paths that resolve outside the manifest directory (`..`, absolute paths, or symlinks) or to a non-regular file; previously, any readable local JSON file could be copied into the result.
- Read input files at most 2 MiB, including FIFOs and devices whose reported size is zero.
- Redact credential headers and secret-like query fields, and drop raw URLs, in every recorded `attempts[]` entry as well as the request. Strip header names before matching, and cover more common names such as `X-Goog-Api-Key`, `X-Auth-Token`, `apiKey`, `client_secret`, and `refresh_token`.
- HTML-escape every summary value in `render` output.
- Report deeply nested input JSON as a concise error instead of a traceback.

### Changed

- A minimal repro now inlines only the divergent probe values, matching the documentation.
- Release notes come from the matching CHANGELOG section, so non-code contributions are credited.
- CI checkouts no longer persist credentials, and the pinned actions are `actions/checkout` v7.0.1 and `actions/setup-python` v7.0.0.
- Moved the repository to `Akhilesh-Gogikar`, removed maintainer launch planning from the repository, linked live contributor issues, and listed related tools only once they are public.
- Clarified the v0 scope: the tool compares captured or adapter-produced observations, and stream modeling is future work.

## [0.1.0] - 2026-08-17

### Added

- Deterministic normalization and semantic comparison for TypeScript, Python, and Go observation slots.
- Captured, inline, and explicitly enabled argv-command adapters.
- Probe categories for defaults, errors, retries, pagination, nullability, and field handling.
- JSON-pointer transforms, baseline-relative diffs, static accessible HTML, and self-contained minimal repros.
- Synthetic offline proof with exactly three intentional divergences.
- Local Python console-package metadata, community policies, CI, and source-only tag release automation.

### Security and privacy

- Common credential headers and secret-like URL query fields are redacted.
- Raw URLs are discarded after normalization; adapter commands remain explicit and unsandboxed.
- Production traffic, credentials, and named provider failure claims remain excluded.

[Unreleased]: https://github.com/Akhilesh-Gogikar/sdk-wirediff/compare/v0.1.1...HEAD
[0.1.1]: https://github.com/Akhilesh-Gogikar/sdk-wirediff/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/Akhilesh-Gogikar/sdk-wirediff/releases/tag/v0.1.0
