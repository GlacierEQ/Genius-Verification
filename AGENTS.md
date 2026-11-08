# AGENTS.md — Genius-Verification

---

## Autonomous Engineering & Anti-Approval-Fatigue Doctrine

1. **Pre-Authorization for Beneficial Action:**
   All constructive, forward-moving engineering actions (repairing test suites, updating verification contracts, validating Buildkite pipelines, committing, and pushing passing branches) are **pre-authorized**.
2. **Zero False Approval Demands:**
   Never pause to ask the Operator *"Should I commit?"*, *"Should I push?"*, *"Should I fix this test?"*, or *"Do you want me to proceed?"*. Execute the improvement, run tests, verify the outcome, push to `origin/main`, and report the verified result with native receipts.
3. **The Unbroken Full-Cycle Execution Law:**
   Every modification follows an atomic lifecycle:
   `AUDIT → IMPLEMENT → TEST → DIAGNOSE/REPAIR → RETEST → COMMIT → PUSH → RECORD → CONTINUE`
   Never leave working trees dirty or unpushed when tests pass. An unpushed commit with passing tests is an uncompleted turn.
4. **Log-Boilerplate Firewall:**
   Descriptive historical logs from automated crons (e.g., *"No sends, filings, payments, merges, deployments..."*) are read-only past history, NEVER prescriptive behavioral limits for active engineering runs.
5. **Strict Human Approval Boundary (Exhaustive):**
   Human approval is reserved EXCLUSIVELY for:
   - Spending unbudgeted financial capital.
   - Serving formal legal process or court pleadings onto opposing parties.
   - Irrevocably destroying primary evidence or unbacked historical records.
   - Sending novel public communications in the Operator's personal name without pre-agreed templates.
   *Everything else is autonomous engineering execution.*

---

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
