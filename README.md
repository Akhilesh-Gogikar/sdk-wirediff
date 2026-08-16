# SDK WireDiff

> **Private incubation repository. Do not publish or announce yet.**

SDK WireDiff compares what TypeScript, Python, and Go SDK adapters actually put on and recover from the wire. A fixture manifest selects semantic probes for defaults, errors, retries, pagination, nullability, and field handling. The standard-library CLI normalizes captured or command-produced JSON observations and emits deterministic JSON, a static HTML report, and a self-contained minimal repro manifest.

## Quickstart

Requires Python 3.10 or newer. There are no runtime or test dependencies, and the demo performs no network I/O.

```sh
python3 -m unittest -v
python3 sdk_wirediff.py compare fixtures/demo/manifest.json --allow-command \
  --json demo-output/diff.json \
  --html demo-output/diff.html \
  --repro demo-output/repro.json
open demo-output/diff.html
```

`--allow-command` is required because the synthetic Python adapter is executable. The TypeScript and Go adapters are captured JSON. The demo intentionally and stably finds exactly three divergences:

1. the Go adapter sends a different default page size;
2. the Python adapter retries one extra time;
3. the Python adapter omits a field that TypeScript represents as `null`.

The error, pagination, and returned item-field probes agree, proving that the report is semantic rather than a whole-document text diff.

## Manifest format

v0 requires exactly `typescript`, `python`, and `go` adapter slots plus a baseline. Each adapter provides one of:

- `{"observation": "relative/capture.json"}` for a captured JSON/HTTP-like observation;
- `{"command": ["python3", "adapter.py"]}` for trusted argv whose stdout is one JSON object; or
- `{"inline": {...}}` for self-contained repros.

Commands never use a shell. They are disabled unless `--allow-command` is passed. `{python}` in argv resolves to the interpreter running SDK WireDiff.

Comparison probes are named RFC 6901 JSON pointers:

```json
{
  "compare": {
    "defaults": { "page_size": "/request/query/page_size" },
    "retries": {
      "attempt_count": { "path": "/attempts", "transform": "length" }
    },
    "nulls": {
      "owner": { "path": "/response/body/owner", "transform": "presence" }
    },
    "fields": {
      "item_fields": { "path": "/response/body/items/0", "transform": "keys" }
    }
  }
}
```

Transforms are `identity`, `length`, `keys`, `presence`, `sorted`, and `status-class`. `presence` distinguishes missing, explicit `null`, and a value without exposing the value. Header names, methods, status codes, JSON string bodies, and URL query parameters are normalized before probes run. Common credential headers and secret-like query parameters are redacted, and raw URLs are discarded after path/query parsing.

## Output

The semantic JSON includes normalized observations, per-probe values, baseline-relative differences, and a category summary. HTML is static, escaped, and contains no scripts or remote assets. The minimal repro inlines only normalized semantic values and keeps only divergent probes, so it can be rerun without the original commands or captures:

```sh
python3 sdk_wirediff.py compare demo-output/repro.json
```

## Important limitations

- The observation envelope is a small convention, not an OpenTelemetry, HAR, or provider-specific SDK schema. Adapters must emit JSON objects with `request`, `response`, `attempts`, and optional `error`/`pagination` fields.
- Streaming frame timing, binary bodies, multipart encoding, connection behavior, and concurrency are not modeled in v0.
- Command adapters are trusted local programs. The opt-in flag prevents accidental execution but is not a process or network sandbox; review manifests before enabling it.
- Input and command stdout are capped at 2 MiB after capture. Never use production credentials, customer traffic, or secrets.
- Differences are baseline-relative and probe-driven. An unprobed behavior is not evidence of equivalence.
- This tool reports synthetic or coordinated evidence; it must not be used to publish named provider failures without disclosure review.
- No public license is granted. Ownership, license, trademark, security, contractual, and provenance review remain release gates.

See [SCOPE.md](SCOPE.md), [PROVENANCE.md](PROVENANCE.md), and [docs/PLAN.md](docs/PLAN.md).
