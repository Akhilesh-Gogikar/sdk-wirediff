# Privacy

SDK WireDiff has no telemetry, analytics, remote assets, hosted service, or built-in network client. Its synthetic demo performs no network I/O.

## Data processed

- Manifests and relative paths.
- Captured, inline, or command-produced observations.
- Normalized requests, responses, attempts, errors, pagination, and selected semantic values.
- Deterministic JSON, HTML, and repro files written to user-selected paths.

Common authorization/cookie/key headers and token-like URL query fields are replaced with `[REDACTED]`; raw URLs are removed after path/query parsing. This is defense in depth, not a complete data-loss-prevention system. Bodies, field names, adapter stderr, paths, and nonstandard secrets may remain.

## Command adapters

An enabled adapter inherits the host environment plus manifest-specified values. It can read files or use the network within host permissions. Do not expose credentials to an adapter and do not run an untrusted manifest. Prefer captures or inline observations.

## Retention

The tool keeps no database. Output remains on disk until the user removes it. A minimal repro avoids original raw captures but can still contain selected semantic values; review before sharing.

Never use production traffic, customer data, or partner schemas in fixtures or issues. Follow [SECURITY.md](../SECURITY.md) for exposure.
