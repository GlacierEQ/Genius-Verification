# AGENTS.md — Genius-Verification

## Buildkite execution contract

Expected pipeline: `casey-1/genius-verification`.

APEX control is external: `GlacierEQ/apex-control-plane/scripts/reconcile_genius_buildkite.py` owns pipeline reconciliation and terminal family verification. This repository owns Verification-domain execution only.

The Verification job must preserve:

- contract validation;
- Python tooling compilation;
- executable contract unit tests;
- JUnit + SHA-256 proof artifacts;
- a host-side terminal receipt bound to those artifacts.

Buildkite's base upload step owns dynamic pipeline parse/secret validation. Do not duplicate that gate inside the repository pipeline.

The Docker job may receive only the nonsecret identity variables it actually needs. Do not use `propagate-environment: true`.

Current production queue: `macos-self`. `oracle-arm64` is not promoted for Genius evidence until live Buildkite proof exists.

A successful claim requires terminal Buildkite PASS and the matching `buildkite/genius-verification` success projection on the exact GitHub SHA, not merely a committed pipeline definition.

Useful commands:

```sh
bk pipeline validate --file .buildkite/pipeline.yml
bk pipeline view casey-1/genius-verification --json
bk build view --pipeline casey-1/genius-verification --summary
```
