# Launch kit

This is an internal readiness and response plan, not authorization to make the repository public. Every public statement must be backed by the synthetic three-divergence fixture or a sanitized, disclosure-safe reproduction.

## Positioning guardrails

**One line:** Compare normalized TypeScript, Python, and Go SDK observations with named semantic probes and generate a minimal replayable diff.

**Differentiator:** SDK WireDiff compares selected meanings—defaults, errors, retries, pagination, nullability, and fields—rather than declaring whole payloads equal or different.

**Demo claim:** The offline fixture intentionally finds exactly three divergences: one default, one retry count, and one missing-versus-null difference.

**Required caveat:** Unprobed behavior is not evidence of equivalence, and explicitly enabled command adapters are trusted local programs rather than a sandbox.

Do not claim adoption, provider correctness, production safety, benchmark superiority, or failures in a named third-party SDK without independent reproduction and coordinated disclosure.

## Proof package before launch

- Run `python3 -m unittest -v`; run the demo twice and compare result JSON byte for byte.
- Replay `demo-output/repro.json` without `--allow-command`; confirm the same three differences.
- Install in an isolated environment; run installed `sdk-wirediff --version`, `--help`, demo, and repro.
- Confirm CI covers the declared `>=3.10,<3.15` range/platform slice and retains pinned action SHAs.
- Check relative links, YAML, secrets/private paths, build metadata, provenance, and git history.
- Manually review keyboard flow, 200% zoom, focus, table reading, color independence, and screen-reader order.
- Confirm ownership, MIT license, advisory route, default branch, and the explicit visibility decision.

## Three-minute demo script

1. **Frame the problem (20 seconds).** “SDKs for the same API can drift in defaults, retry policy, nullability, errors, pagination, or returned fields.”
2. **Show the contract (30 seconds).** Open `fixtures/demo/manifest.json`; point to the three language slots, TypeScript baseline, and six named probe categories.
3. **Run the proof (20 seconds).** Execute the copy-paste comparison command from the README.
4. **Read the report (45 seconds).** Open `demo-output/diff.html`; show Go’s page-size default and Python’s retry and missing-owner differences. Note that error, pagination, and item-field probes agree.
5. **Inspect evidence (30 seconds).** Open `diff.json`; show normalized observations, baseline/adapter values, deterministic ordering, and summary count.
6. **Replay without code (30 seconds).** Run `sdk-wirediff compare demo-output/repro.json`; explain that the repro contains normalized semantic values and executes no adapter.
7. **State limits (30 seconds).** Probe-driven, fixed three-language v0, no production traffic, command adapters are opt-in and unsandboxed, redaction is defense in depth.
8. **Invite one action (15 seconds).** Point to [prepared issue seeds](ISSUE_SEEDS.md), especially pointer tests and bounded stdout streaming.

## Copy for launch channels

Use one primary launch and adapt responses instead of repeating identical promotion. Disclose that you are the maintainer.

### Hacker News

**Title:** `Show HN: SDK WireDiff – semantic diffs across TypeScript, Python, and Go clients`

**Text:**

> I built SDK WireDiff to test a narrow question: when three SDKs make an equivalent call, do their normalized wire behaviors agree on defaults, errors, retries, pagination, nullability, and fields?
>
> A manifest selects named probes. The CLI compares each adapter with a baseline, emits deterministic JSON and static HTML, then writes a minimal repro that can replay divergent semantics without rerunning adapter commands.
>
> The included offline fixture intentionally finds exactly three differences. It contains no production traffic or provider claim, and unprobed behavior is not treated as equivalent. I would value critique of the semantic model and the prepared pointer, process-bound, and schema issues.

### Reddit

**Title:** `I made an offline semantic diff for TypeScript, Python, and Go SDK behavior`

**Text:**

> Maintainer here. SDK WireDiff uses named JSON-pointer probes to compare defaults, retries, errors, pagination, nullability, and fields across three SDK observations.
>
> The demo is deliberately synthetic: one default mismatch, one retry mismatch, and one missing-versus-null mismatch. It also generates a self-contained repro that executes no original adapter.
>
> This is not a traffic recorder, provider leaderboard, or equivalence proof for fields you did not probe. I’m looking for technical feedback and contributors for five scoped issues, from pointer edge cases to bounded subprocess streaming.

### LinkedIn

> Open-source launch candidate: SDK WireDiff.
>
> Generated and hand-written SDKs can drift independently in defaults, retries, errors, pagination, nullability, and returned fields. SDK WireDiff turns those assumptions into named semantic probes and a deterministic, replayable report across TypeScript, Python, and Go observations.
>
> The offline fixture intentionally demonstrates exactly three differences. No production traffic, provider ranking, or adoption claim is involved.
>
> I’ve added a contributor ladder and five code-aware issue drafts for testing, subprocess safety, and schema design. I’m the maintainer and welcome evidence-based critique.

### X

**Post 1:** `Equivalent SDK method names do not guarantee equivalent wire behavior. SDK WireDiff compares named semantics across TypeScript, Python, and Go observations.`

**Post 2:** `The offline demo intentionally finds 3 differences: a default, a retry count, and missing-vs-null. Output is deterministic JSON + static HTML + a repro that reruns no adapter code.`

**Post 3:** `Limits are explicit: probe-driven, fixed 3-language v0, no production traffic, commands opt-in and not sandboxed. Feedback + five scoped issues: https://github.com/akigogikar/sdk-wirediff`

## FAQ

**Why not diff the entire JSON document?** Whole-document diffs mix semantic changes with headers, ordering, naming, and irrelevant fields. Named probes state which behavior matters.

**Does no diff mean the SDKs are equivalent?** No. It means configured probes produced equal normalized values for this fixture.

**Why exactly three language slots?** A fixed matrix keeps the first proof inspectable. Another slot requires a proof fixture and governance decision.

**Does the minimal repro run adapter code?** No. It inlines normalized semantic values and keeps divergent probes.

**Are command adapters safe?** They are argv-only and opt-in, but run with host permissions. Review them and use a controlled environment.

**Can I submit production traffic?** No. Use synthetic or sanitized public observations. Redaction covers common fields but is not complete data-loss prevention.

## Launch-day checklist

- [ ] Re-run the proof package at the intended commit; keep results internally.
- [ ] Confirm repository visibility, advisory route, branch rules, CI, license detection, and 0.1.0 metadata.
- [ ] Create five issues using the exact prepared titles/labels; replace document-only references with issue links where useful.
- [ ] Prepare only synthetic report images with useful alt text and no local paths.
- [ ] Publish one primary post, disclose maintainer status, and stay available for technical questions.
- [ ] Route named-provider or sensitive claims into coordinated review rather than public debate.
- [ ] Convert reproducible defects into minimal fixtures; correct documentation quickly.

## First 30 days

### Days 1–3

- Triage actionable reports daily when possible; keep security and disclosure-sensitive material private.
- Replay every claimed difference with synthetic/sanitized evidence before confirming it.
- Turn repeated confusion into one README/FAQ fix.

### Week 1

- Release corrections only when evidence requires them; do not tag for attention.
- Welcome contributors with bounded issues and review against the seven-day triage target.
- Measure useful signals: successful repro replay, clarified probes, reduced false positives, and disclosure-safe issue quality—not stars.

### Weeks 2–4

- Publish a transparent summary of verified differences, false positives, and unresolved design questions without naming providers.
- Move issue seeds through the contributor ladder only when acceptance tests are unambiguous.
- Revisit roadmap order using reproduced pain, privacy risk, maintenance cost, and reviewer capacity.
- Review command safety, redaction feedback, dependencies, advisories, CI, accessibility, and contributor recognition.
- Decide whether evidence supports 0.1.x hardening, a narrow 0.2 proposal, or no expansion.

## Social preview and media

- Upload [the 1280 × 640 PNG](assets/social-preview.png) in **Settings → General → Social preview** immediately before the visibility change; GitHub does not read this repository file automatically.
- Keep the adjacent SVG as the editable source and follow the [asset notes](assets/README.md).
- Capture demos with synthetic inputs only. Remove usernames, home paths, tokens, partner names, and unrelated windows.
- Provide captions, a transcript, and descriptive alt text. Verify the README image, generated HTML, and demo at 200% zoom, by keyboard, and with a real screen reader before posting.
- Do not place download, adoption, company, performance, or compatibility counts on an asset unless the source and date are public and reproducible.

## Ethical cross-promotion

Cross-link only the seven related OSS tools named in ECOSYSTEM.md, and only where a link answers the reader's next technical question. Links stay optional, disclosed, and outside runtime output. Commercial products require exact owner-approved names, URLs, relationship wording, and trademark or partner permission before inclusion.
