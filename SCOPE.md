# Scope

## Purpose

API documentation, schemas, generated clients, hand-written SDKs, and real wire behavior drift independently.

## v0 boundary

- Describe one behavior fixture and compare captured or adapter-produced observations from TypeScript, Python, and Go clients.
- Normalize HTTP-like observations and compare defaults, retries, errors, pagination, nullability, and field handling. Stream modeling is future work.
- Render a semantic diff with a minimal reproducer.

## Explicit non-goals

- A generic API gateway or hosted traffic recorder.
- Publishing named provider failures without coordinated disclosure.
- Using production credentials or customer traffic.

## Clean-room exclusions

- No source, fixtures, prompts, traces, schemas, requirements, or examples from private company, partner, customer, or unpublished research repositories.
- No customer or partner names, data, incidents, screenshots, or derived requirements.
- No public release until ownership, license, trademark, security, and contractual reviews are recorded (see the launch review in [PROVENANCE.md](PROVENANCE.md)).

## First proof gate

A synthetic API fixture demonstrates three intentional cross-SDK divergences with stable, explainable diffs.
