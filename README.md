# SDK WireDiff

[![CI](https://github.com/akigogikar/sdk-wirediff/actions/workflows/ci.yml/badge.svg)](https://github.com/akigogikar/sdk-wirediff/actions/workflows/ci.yml)
[![License](https://img.shields.io/github/license/akigogikar/sdk-wirediff)](LICENSE)

> **Status:** 0.1.0 launch candidate in a private repository. It is suitable for synthetic and sanitized public observations, but has not completed the owner’s public-launch review and is not published to a package registry.

SDK WireDiff compares what TypeScript, Python, and Go SDK adapters put on and recover from the wire. A fixture manifest selects semantic probes for defaults, errors, retries, pagination, nullability, and field handling. The standard-library CLI normalizes captured or command-produced JSON observations and emits deterministic JSON, a static HTML report, and a self-contained minimal repro.

## Install from a local checkout

Requires Python 3.10 through 3.14 (`>=3.10,<3.15`). CI tests all five versions on Linux and Python 3.14 on macOS and Windows. There are no runtime dependencies.

```sh
git clone https://github.com/akigogikar/sdk-wirediff.git
cd sdk-wirediff
python3 -m pip install --no-deps .
sdk-wirediff --help
```

Use a virtual environment for an isolated install. For a repository-only workflow, replace `sdk-wirediff` below with `python3 sdk_wirediff.py`.

## One-command semantic comparison

The demo is synthetic and performs no network I/O. It intentionally finds exactly three differences.

```sh
sdk-wirediff compare fixtures/demo/manifest.json --allow-command \
  --json demo-output/diff.json \
  --html demo-output/diff.html \
  --repro demo-output/repro.json
```

Open `demo-output/diff.html` locally. `--allow-command` is required because the synthetic Python adapter is executable; TypeScript and Go use captured JSON.

The expected differences are:

1. Go sends a different default page size.
2. Python retries one extra time.
3. Python omits a field that TypeScript represents as `null`.

Errors, pagination, and returned item fields agree, demonstrating a probe-driven semantic diff rather than a whole-document text diff.

Replay the generated, self-contained repro without executing adapters:

```sh
sdk-wirediff compare demo-output/repro.json
```

## Manifest

Version 0 requires exactly `typescript`, `python`, and `go` adapter slots plus a baseline. Each adapter provides one of:

- `{"observation": "relative/capture.json"}` for captured JSON;
- `{"command": ["python3", "adapter.py"]}` for trusted argv whose stdout is one JSON object; or
- `{"inline": {...}}` for self-contained repros.

Commands never use a shell and are disabled unless `--allow-command` is passed. `{python}` resolves to the interpreter running SDK WireDiff.

Named RFC 6901 probes select semantics:

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

Transforms are `identity`, `length`, `keys`, `presence`, `sorted`, and `status-class`. `presence` distinguishes missing, explicit `null`, and a value without exposing the value. Header names, methods, statuses, JSON string bodies, and URL queries are normalized first. Common credential headers and secret-like query parameters are redacted; raw URLs are discarded after path/query parsing.

## Honest boundaries

- The observation envelope is a small convention, not a general traffic or telemetry standard.
- Streaming frame timing, binary/multipart bodies, connection behavior, and concurrency are not modeled in 0.1.x.
- Command adapters are trusted local programs. The opt-in flag prevents accidental execution but is not a process or network sandbox.
- Input and command stdout are capped at 2 MiB after capture. Never use production credentials, customer traffic, or secrets.
- Differences are baseline-relative and probe-driven. Unprobed behavior is not evidence of equivalence.
- Do not publish named provider failures without coordinated disclosure and independent reproduction.
- A generic gateway, hosted recorder, or production capture agent is out of scope.

## Project navigation

- Design: [architecture](docs/ARCHITECTURE.md), [API stability](docs/API_STABILITY.md), [roadmap](ROADMAP.md)
- Operations: [troubleshooting](docs/TROUBLESHOOTING.md), [privacy](docs/PRIVACY.md), [accessibility](docs/ACCESSIBILITY.md)
- Community: [contributing](CONTRIBUTING.md), [conduct](CODE_OF_CONDUCT.md), [support](SUPPORT.md), [governance](GOVERNANCE.md)
- Safety: [security policy](SECURITY.md), [provenance](PROVENANCE.md), [scope](SCOPE.md)
- Release: [changelog](CHANGELOG.md), [launch kit](docs/LAUNCH_KIT.md), [MIT license](LICENSE)
- Related experiments: [optional ecosystem map](ECOSYSTEM.md)

Security vulnerabilities should be reported through a [private security advisory](https://github.com/akigogikar/sdk-wirediff/security/advisories/new), never a public issue.
