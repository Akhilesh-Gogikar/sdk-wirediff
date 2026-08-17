# Contributing to SDK WireDiff

SDK WireDiff accepts narrow contributions that make cross-language behavior evidence more precise and reproducible. Start substantial work with an issue so the proposal can be checked against [SCOPE.md](SCOPE.md), the fixed v0 language matrix, and the [roadmap](ROADMAP.md).

## Local setup

1. Use Python 3.10–3.14; versions outside the declared `>=3.10,<3.15` range are not supported.
2. Run `python3 -m pip install --no-deps .` in a virtual environment if you need the console command.
3. Run `python3 -m unittest -v` and the synthetic demo before editing.
4. Demonstrate the behavior with the smallest synthetic or sanitized public observation.

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

Explain the semantic behavior, observation provenance, risk, and rollback. Keep unrelated adapter or formatting changes out. By contributing, you agree that your contribution is licensed under the repository’s [MIT License](LICENSE) and that you have the right to submit it.
