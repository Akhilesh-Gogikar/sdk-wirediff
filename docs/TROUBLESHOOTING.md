# Troubleshooting

## `pass --allow-command for trusted fixtures`

At least one adapter uses `command`. Review the manifest and executable first. If it is trusted and requires no production credentials, rerun with `--allow-command`. Prefer captured JSON when execution is unnecessary.

## The command stdout is not one JSON object

Remove banners and diagnostic logging from stdout; send diagnostics to stderr. The adapter must exit zero and emit exactly one object no larger than 2 MiB.

## A probe is always `missing`

Inspect the normalized observation in result JSON, then verify RFC 6901 escaping: `~1` represents `/` and `~0` represents `~`. Array positions are decimal indices. A raw capture path may differ after URL/body normalization.

## `presence` and `identity` disagree

`presence` intentionally returns `missing`, `null`, or a value type. `identity` compares the actual normalized value. Use `presence` for nullability contracts and `identity` only when the value itself is semantic.

## The minimal repro adds or loses a difference

Confirm it was produced by the same 0.1.x version and was not edited. A repro inlines normalized semantics and retains only divergent probes; it does not rerun the original adapters.

## Sensitive data appears in output

Stop sharing the artifact and follow [SECURITY.md](../SECURITY.md). Built-in redaction covers common credential headers and secret-like query fields, not arbitrary body keys or adapter logs. Use only synthetic/sanitized captures.

Run the documented synthetic demo to distinguish an installation problem from a fixture problem. File sanitized issues under [SUPPORT.md](../SUPPORT.md).
