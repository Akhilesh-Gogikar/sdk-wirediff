# Architecture

SDK WireDiff is one Python standard-library module plus a console entry point. Its fixed three-language matrix and fixture-driven design make each semantic claim inspectable.

## Data flow

`manifest → adapter loading → HTTP-like normalization → named probes/transforms → baseline comparison → deterministic JSON + static HTML + inline repro`

## Components

1. **Manifest loader** requires TypeScript, Python, and Go slots, one baseline, and named probe categories.
2. **Adapter loader** accepts a relative JSON capture, inline object, or explicitly enabled argv command. Commands use no shell and must emit one bounded JSON object.
3. **Normalizer** canonicalizes method, status, header names, JSON-like bodies, URL path/query, attempts, common error/pagination shapes, and sensitive header/query values.
4. **Probe engine** traverses RFC 6901 pointers and applies `identity`, `length`, `keys`, `presence`, `sorted`, or `status-class`.
5. **Comparator** evaluates every non-baseline adapter against the baseline in a stable category/probe/language order.
6. **Report/repro writers** escape static HTML and inline only normalized semantic values needed to replay divergent probes.

## Determinism and trust

Canonical JSON sorts object keys and preserves intentional array order. Results omit timings and generation timestamps. Captures are data; enabled command adapters are executable code with host permissions. The opt-in flag is a guard against accidental execution, not a sandbox.

See [PRIVACY.md](PRIVACY.md), [SECURITY.md](../SECURITY.md), and [API_STABILITY.md](API_STABILITY.md).
