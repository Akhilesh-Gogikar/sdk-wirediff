# Issue seeds

These mirror the five contributor-ready GitHub issues and preserve their design context; the [live ready-for-contribution list](https://github.com/Akhilesh-Gogikar/sdk-wirediff/issues?q=is%3Aissue+is%3Aopen+label%3A%22status%3A+ready%22) is authoritative for assignment, labels, and status. Confirm the code still matches each seed before contributing. All observations must be synthetic or sanitized public material; never attach production traffic or credentials.

## 1. List valid transforms when a manifest uses an unknown transform

**Issue:** [#4](https://github.com/Akhilesh-Gogikar/sdk-wirediff/issues/4)

**Labels:** `cli`, `difficulty: beginner`, `good first issue`, `help wanted`, `mentored`, `size: S`, `status: ready`, `tests`

**Milestone:** v0.2 — community evidence

**Rationale:** `transform_value` reports the unsupported name but does not tell the fixture author which transforms are valid. The allowed set is small and stable within 0.1.x, so the error can be actionable without a dependency.

**Acceptance criteria:**

- The error names the category/probe, rejected transform, and all valid transform names in deterministic order.
- Valid-transform data has one source of truth rather than a second list that can drift.
- Existing successful output and exception type remain unchanged.
- Add focused tests for an unknown transform and every supported transform name.

**Test plan:** Run `python3 -m unittest -v`; invoke a temporary manifest with `transform: unknown` and assert nonzero exit plus the complete hint.

**Skills:** Introductory Python, error design, `unittest`.

**Estimated scope:** 2–4 hours.

**Likely files:** `sdk_wirediff.py`, `test_sdk_wirediff.py`.

## 2. Add a table-driven JSON Pointer edge-case matrix

**Issue:** [#5](https://github.com/Akhilesh-Gogikar/sdk-wirediff/issues/5)

**Labels:** `difficulty: beginner`, `good first issue`, `help wanted`, `json-pointer`, `mentored`, `size: M`, `status: ready`, `tests`

**Milestone:** v0.2 — community evidence

**Rationale:** The demo covers ordinary object and array paths, while `pointer_get` also implements escaped `/` and `~`, invalid indices, scalar traversal, empty pointer, missing, and explicit null. Those distinctions deserve a compact conformance table.

**Acceptance criteria:**

- Add table-driven cases for `~1`, `~0`, empty pointer, arrays, invalid/negative/out-of-range indices, scalar traversal, missing keys, and null values.
- Assert missing remains distinct from explicit null after `identity` and `presence` transforms.
- Use only inline synthetic values; do not broaden the pointer syntax beyond RFC 6901.
- Fix implementation only if a test demonstrates a real discrepancy.

**Test plan:** Run the focused table on Python 3.10 and 3.14, then the full suite and three-divergence demo.

**Skills:** Python testing, JSON Pointer basics, boundary analysis.

**Estimated scope:** 3–6 hours.

**Likely files:** `test_sdk_wirediff.py`, `sdk_wirediff.py` only if needed.

## 3. Cover command timeout and nonzero-exit contracts with synthetic adapters

**Issue:** [#6](https://github.com/Akhilesh-Gogikar/sdk-wirediff/issues/6)

**Labels:** `adapters`, `difficulty: intermediate`, `help wanted`, `reliability`, `size: M`, `status: ready`, `tests`

**Milestone:** v0.2 — community evidence

**Rationale:** The command adapter is opt-in and handles timeout, spawn failure, nonzero exit, stderr truncation in its error, and malformed stdout, but the synthetic proof currently covers only successful execution and refusal without consent.

**Acceptance criteria:**

- Add small synthetic adapters for timeout, nonzero exit with stderr, and malformed JSON stdout.
- Assert concise `WireDiffError` messages without leaking environment variables or unrelated output.
- Keep the suite offline, bounded, and fast; use a timeout with enough CI margin.
- Ensure temporary processes are reaped on every platform in the supported matrix.
- Document the failure contract in troubleshooting if tests reveal ambiguity.

**Test plan:** Run focused cases repeatedly on Linux, then the platform CI matrix; run the existing demo and confirm its exact three differences.

**Skills:** Python subprocesses, portable fixtures, error-path testing.

**Estimated scope:** 1–2 days.

**Likely files:** `test_sdk_wirediff.py`, new `fixtures/command-errors/` scripts, `sdk_wirediff.py` only for demonstrated bugs, `docs/TROUBLESHOOTING.md`.

## 4. Enforce the adapter stdout limit while streaming

**Issue:** [#7](https://github.com/Akhilesh-Gogikar/sdk-wirediff/issues/7)

**Labels:** `advanced`, `difficulty: advanced`, `help wanted`, `performance`, `security`, `size: L`, `status: ready`

**Milestone:** v0.2 — community evidence

**Rationale:** `load_adapter` currently uses `subprocess.run(..., capture_output=True)` and checks the 2 MiB limit after the child exits. A noisy or hostile trusted adapter can consume unbounded memory before rejection. The limit should apply during capture.

**Acceptance criteria:**

- Replace unbounded capture with a standard-library streaming design that stops reading and terminates the child once stdout exceeds 2 MiB.
- Bound retained stderr independently while preserving a useful error tail.
- Avoid pipe deadlocks; reap the process on success, overflow, timeout, and parse failure across supported platforms.
- Preserve successful adapter semantics, `{python}`, cwd/env behavior, and concise `WireDiffError` output.
- Update privacy/security/architecture text from “capped after capture” to the implemented behavior.

**Test plan:** Synthetic children produce output just below, exactly at, and above the limit while also writing stderr; monitor completion and result/error; run full platform matrix and existing demo.

**Skills:** Advanced Python subprocess I/O, concurrency/selectors or threads, resource bounds, cross-platform testing.

**Estimated scope:** 3–5 days including review.

**Likely files:** `sdk_wirediff.py`, `test_sdk_wirediff.py`, new bounded-output fixtures, `docs/ARCHITECTURE.md`, `docs/PRIVACY.md`, `SECURITY.md`.

## 5. Define versioned schemas for manifests, observations, results, and repros

**Issue:** [#8](https://github.com/Akhilesh-Gogikar/sdk-wirediff/issues/8)

**Labels:** `advanced`, `api`, `design`, `difficulty: advanced`, `documentation`, `size: L`, `status: ready`

**Milestone:** v0.2 — community evidence

**Rationale:** Runtime validation and examples define the current envelopes, but adapter authors lack machine-readable contracts. Separate schemas can clarify input versus normalized output without implying that arbitrary command execution is safe.

**Acceptance criteria:**

- Discuss the schema split and compatibility policy in the issue before implementation.
- Add versioned schemas for manifests, raw observation envelopes, `schemaVersion: 1` results, and self-contained repro manifests.
- Cover exactly the TypeScript/Python/Go slots, one adapter source mode, probe specifications/transforms, missing/null encodings, diffs, and extensible normalized fields.
- Validate the demo and generated repro in a dependency-free test or a clearly justified development-only approach.
- Document what schema validation cannot guarantee: credential absence, command safety, semantic completeness, or provider correctness.

**Test plan:** Positive checks for demo inputs/outputs and replay; negative checks for multiple adapter modes, unknown transforms, absent baseline slots, and malformed diffs; all existing tests remain deterministic.

**Skills:** JSON Schema, API design, semantic versioning, privacy-aware documentation.

**Estimated scope:** 3–4 days including design review.

**Likely files:** new `schemas/` files, `test_project_metadata.py` or a focused schema test, `docs/API_STABILITY.md`, `docs/ARCHITECTURE.md`, `README.md`.
