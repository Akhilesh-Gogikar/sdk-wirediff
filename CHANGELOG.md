# Changelog

All notable changes are recorded here. The project follows semantic versioning while pre-1.0 compatibility remains intentionally limited; see [API_STABILITY.md](docs/API_STABILITY.md).

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

[0.1.0]: https://github.com/akigogikar/sdk-wirediff/releases/tag/v0.1.0
