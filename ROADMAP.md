# Roadmap

This roadmap is directional, not a delivery promise. Reproducible semantic evidence outranks dates.

## 0.1.x — harden the three-language proof

- Publish example observation and result schemas with compatibility fixtures.
- Add adversarial JSON-pointer, redaction, malformed-body, command-timeout, and output-limit tests.
- Improve diff grouping and accessible navigation for larger probe sets.
- Document adapter authoring patterns for captured and command-produced observations.
- Build a sanitized public benchmark only after coordinated review.

The contribution-ready slice is maintained in [ISSUE_SEEDS.md](docs/ISSUE_SEEDS.md). Pointer/report tests are the first rung, bounded execution work is help-wanted, and schema work requires design review. An item joins 0.1.x only with a synthetic proof, deterministic test, privacy review, and named reviewer.

## Candidate 0.2 work

- Compare more than one baseline without hiding pairwise evidence.
- Add deterministic stream-frame envelopes without modeling wall-clock timing.
- Explore machine-readable policy for intentionally tolerated differences.

## Not planned in this roadmap

A generic gateway, hosted recorder, transparent production interception, provider leaderboard, credential manager, or automatic execution sandbox is out of scope. Additional language slots require a new proof fixture and governance decision.
