# API stability

SDK WireDiff is pre-1.0. Compatibility is deliberate but not yet permanent.

## Stable within 0.1.x

- Console commands `compare` and `render` and their documented flags.
- Exit status zero on success and nonzero on rejected input or failed operation.
- The tested Python runtime range `>=3.10,<3.15` (Python 3.10 through 3.14).
- The required TypeScript/Python/Go adapter slots, baseline, six probe categories, RFC 6901 paths, and documented transforms.
- Result `schemaVersion: 1`, baseline-relative `diffs`, `summary`, and canonical JSON.

Patch releases may add optional fields and validation without changing existing meaning. Consumers must ignore unknown object fields.

## Allowed before 1.0

A minor release may tighten an unsafe envelope, redaction rule, or transform after changelog and migration notes. Human-readable stderr, HTML markup/classes/CSS, source metadata, normalization internals, and importable helper functions are not stable APIs. The HTML is for people, not scraping.

Deprecations should span at least one minor release when security and correctness permit. Immediate security fixes may break unsafe behavior.
