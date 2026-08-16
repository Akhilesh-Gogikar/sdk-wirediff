# SDK WireDiff

> **Private incubation repository. Do not publish or announce yet.**

Cross-SDK differential testing for documentation, schemas, clients, and wire behavior.

## Problem

API documentation, schemas, generated clients, hand-written SDKs, and real wire behavior drift independently.

## Planned v0

- Describe one behavior fixture and run equivalent calls through TypeScript, Python, and Go clients.
- Normalize HTTP/stream transcripts and compare defaults, retries, errors, pagination, nullability, and field handling.
- Render a semantic diff with a minimal reproducer.

## Non-goals

- A generic API gateway or hosted traffic recorder.
- Publishing named provider failures without coordinated disclosure.
- Using production credentials or customer traffic.

## Repository state

This repository contains only the clean-room project brief and planning scaffold. No implementation has started.

- Scope and exclusions: [SCOPE.md](SCOPE.md)
- Source/provenance log: [PROVENANCE.md](PROVENANCE.md)
- Initial execution plan: [docs/PLAN.md](docs/PLAN.md)

## Licensing

No public license is granted while this repository is private. Select an OSS license only after ownership and third-party provenance review.
