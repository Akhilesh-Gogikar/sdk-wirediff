# Contributing to SDK WireDiff

SDK WireDiff accepts narrow contributions that make cross-language behavior evidence more precise and reproducible. Start substantial work with an issue so the proposal can be checked against [SCOPE.md](SCOPE.md), the fixed v0 language matrix, and the [roadmap](ROADMAP.md).

## Local setup

1. Use Python 3.10–3.14; versions outside the declared `>=3.10,<3.15` range are not supported.
2. Run `python3 -m pip install --no-deps .` in a virtual environment if you need the console command.
3. Run `python3 -m unittest -v` and the synthetic demo before editing.
4. Demonstrate the behavior with the smallest synthetic or sanitized public observation.

## Contributor pathways

Choose the smallest rung that fits the evidence you want to improve; the ladder is a navigation aid, not a status system.

1. **Reproducer / documenter (`good first issue`)** — add a pointer edge case, improve a probe explanation, test a zero-diff report, or clarify an error. Typical scope: a few hours and one or two files.
2. **Fixture / implementation contributor (`help wanted`)** — add a synthetic adapter failure, timeout, normalization case, or report behavior. Typical scope: one to two focused days.
3. **Design contributor (`advanced`)** — propose streaming bounds, versioned schemas, compatibility policy, or new semantic envelopes. Begin with a written design and synthetic proof.
4. **Reviewer / steward** — replay repros, verify privacy/redaction, check baseline semantics and accessibility, then help triage related reports.

The [prepared issue seeds](docs/ISSUE_SEEDS.md) provide five concrete starting points with acceptance criteria and likely files. When a corresponding issue exists, comment with your intended approach before coding. If a claimed issue has no update for 14 days, another contributor may ask to continue it.

## Triage and recognition

The maintainer targets an initial label/scope response within seven calendar days, but this is not an SLA. Security and disclosure-sensitive reports stay private. Triage prioritizes synthetic reproduction, one semantic question per issue, and reviewable changes inside the three-language boundary.

Merged contributors are credited in commit history and material release notes. Repeat fixture authors and reviewers may be acknowledged in releases and invited to review their demonstrated area. Recognition never requires a real name, employer, or production-data disclosure.

## Clean-room requirements

- Do not contribute production traffic, provider credentials, private schemas, prompts, traces, customer/partner data, or unpublished requirements.
- Do not name a provider in a failure claim without coordinated disclosure and reproducible public evidence.
- Record each public specification, fixture, dataset, or generated asset in [PROVENANCE.md](PROVENANCE.md), including terms.
- Report vulnerabilities privately under [SECURITY.md](SECURITY.md).

## Engineering expectations

- Prefer the Python standard library. A new runtime dependency needs a concrete security and maintenance case.
- Keep adapter commands argv-only, explicitly enabled, bounded, and deterministic. They are never a substitute for sandboxing.
- Preserve missing-versus-null semantics and baseline-relative, probe-driven output.
- Add one small runnable test for non-trivial normalization or transform logic.
- Update privacy and accessibility documentation when capture or report behavior changes.
- Run `python3 -m unittest -v`, the demo/repro flow, an isolated install smoke, and `git diff --check` before a pull request.

## Pull requests

Explain the semantic behavior, observation provenance, risk, and rollback; link the issue with `Closes #…`. Keep unrelated adapter or formatting changes out. By contributing, you agree that your contribution is licensed under the repository’s [MIT License](LICENSE) and that you have the right to submit it.
