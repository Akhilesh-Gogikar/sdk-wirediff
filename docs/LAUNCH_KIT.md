# Launch kit

This is an internal readiness checklist, not authorization to make the repository public.

## Proof package

- Run `python3 -m unittest -v` across the documented Python/platform CI matrix.
- Run the synthetic demo twice and compare JSON byte for byte.
- Replay `demo-output/repro.json` without `--allow-command`; confirm the same three differences.
- Install in a clean virtual environment, run `sdk-wirediff --help`, the demo, and the repro.
- Review both reports using keyboard, 200% zoom, color-independent reading, and a screen reader.
- Run path/link, workflow syntax, secret/private-identifier, build-metadata, provenance, and git-history checks.

## Release review

- Confirm ownership, MIT license, name, branch protection, security advisories, and the explicit private/public decision.
- Ensure `pyproject.toml` and `CHANGELOG.md` agree with the intended `v0.1.0` tag.
- Verify the tag workflow only tests and creates a source release; it must not upload a package registry artifact.
- Use only synthetic demo output in screenshots and examples.
- Avoid provider scorecards, production-readiness claims, adoption claims, or named failure accusations.

## Honest launch copy

**Short description:** “Compare normalized TypeScript, Python, and Go SDK observations with named semantic probes and generate a minimal replayable diff.”

**Demo claim:** “The included offline fixture intentionally finds one default, one retry, and one missing-versus-null divergence.”

**Required caveat:** “SDK WireDiff compares selected normalized observations; unprobed behavior is not evidence of equivalence, and command adapters are not sandboxed.”

## After launch

Prioritize independent synthetic reproductions, disclosure-safe corrections, probe quality, and false-positive reduction rather than attention metrics.
