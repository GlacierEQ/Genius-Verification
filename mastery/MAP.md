# Mastery Map — Genius-Verification

## Epistemic foundation

All Verification-domain work is governed by [`EPISTEMOLOGY.md`](EPISTEMOLOGY.md).

Prime law:

> Verification never proves more than the specification, model, oracle, explored state space, and execution environment actually support.

Every serious verification result must make explicit:

```text
SYSTEM + PROPERTY + ASSUMPTIONS + MODEL + EVIDENCE → JUSTIFIED CLAIM
```

The standing loop is:

```text
SPECIFY → MODEL → GENERATE/EXPLORE → OBSERVE → CHECK → CHALLENGE
       → MINIMIZE COUNTEREXAMPLE → REPRODUCE → PRESERVE RECEIPT → REVISE
```

## Irreducible questions

1. What exact proposition must hold: safety, liveness, functional correctness, security, recovery, memory safety, or performance envelope?
2. Is the specification itself adequate, non-vacuous, and faithful to the intended system?
3. Which verification method matches the risk, oracle, semantic model, and reachable state space?
4. What are the method's soundness, completeness, precision, coverage, and trusted-base limits?
5. Is the evidence exhaustive over a model, sampled over executions, bounded, or observational?
6. What counterexample would falsify the claim, and how will it be preserved and minimized?
7. How does evidence about an abstract model transfer or refine to source, binary, runtime, and deployment?
8. Can the result be reproduced from SHA-bound source, tools, configuration, seeds/models, environment, and artifacts?
9. When does a PASS *not* justify the claim because of oracle weakness, generator gaps, flaky execution, shared failure modes, stale assumptions, or model drift?
10. What remains explicitly unverified after the run?

## Method surfaces

| Method | Primary epistemic use | Characteristic limitation |
|---|---|---|
| Example / unit tests | Named behavior, regressions | Human-selected executions |
| Integration tests | Boundary contracts | Limited environment/state exploration |
| Property-based tests | General predicates across generated inputs | Generator/oracle quality bounds reach |
| Coverage-guided fuzzing | Adversarial path discovery | Sampled executions; harness-dependent |
| Sanitizers | Runtime violation detection | Only reached paths + configured detector class |
| Static analysis | Abstract whole-program reasoning | Soundness/precision/model tradeoffs |
| Differential testing | Independent implementation disagreement | Shared defects reduce independence |
| Model checking | Exhaustive checking of finite model/state space | Model fidelity + bounds/abstraction |
| Deductive verification | Proof of implementation vs specification | Specification/trusted-base/refinement assumptions |
| Interactive theorem proving | Machine-checked mathematical proof | Formalization and trusted kernel remain critical |
| Fault injection | Recovery and resilience properties | Fault model and oracle must be explicit |
| Mutation testing | Oracle/test-suite strength | Mutation operators are proxies, not real defect distribution |
| Production observability | Deployed behavior evidence | Observational; cannot enumerate unseen executions |

## Proof-strength ladder

Do not treat this as a simplistic ranking; use orthogonal evidence. For high-consequence claims, move from local observations toward broader and more independent evidence:

```text
examples
  → properties
  → generated/adversarial exploration
  → instrumentation/static analysis
  → explicit state models
  → model checking / deductive proof where justified
  → fault/recovery experiments
  → exact-runtime readback
```

A higher layer does not erase contradictions discovered below it.

## Counterexample law

One valid counterexample defeats a universal claim. Every counterexample should become durable state:

```text
input / trace / model state
  → minimal reproducer
  → claim linkage
  → root-cause analysis
  → regression or proof obligation
  → fix evidence
  → retained historical counterevidence
```

## Receipt contract

Material verification runs should emit receipts binding:

- `claim_id` and property/specification version;
- source SHA and artifact hashes;
- tool + version;
- exact command/configuration;
- compiler/runtime/dependency versions;
- platform/environment;
- model bounds, seeds, corpus, dictionaries, schedules, or injected faults;
- timestamps and exit status;
- structured results plus stdout/stderr where useful;
- counterexamples/minimized reproducers;
- interpretation, assumptions, and limits.

Green UI state without this binding is routing evidence, not terminal proof.

## Domain mastery targets

### Specification and oracle design
Formal and executable requirements, invariants, temporal properties, adversary/fault models, metamorphic relations, reference models, vacuity detection.

### Property-based testing
Generator design, distributions, shrinking, stateful properties, model-based testing, metamorphic properties, statistical interpretation.

### Fuzzing
Coverage-guided, grammar/structure-aware, stateful and differential fuzzing; harness quality, corpus engineering, crash minimization.

### Sanitizers and runtime instrumentation
ASan, UBSan, TSan, MSan and related detector semantics, blind spots, suppressions, optimization/platform effects.

### Static program analysis
Abstract interpretation, dataflow, aliasing, taint, symbolic execution, path/interprocedural sensitivity, CodeQL-class analyses, soundness/precision tradeoffs.

### Model checking
State-transition systems, temporal logic, safety/liveness, fairness, symmetry reduction, bounded vs exhaustive search, counterexample traces.

### Deductive verification
Pre/postconditions, invariants, frames, termination, SMT-backed verification conditions, proof automation, ghost state.

### Interactive theorem proving
Dependent type theory, proof terms, trusted kernels, tactics, theorem statement adequacy, extraction/refinement boundaries.

### Differential and metamorphic testing
Independent implementations, versions, compilers, models, invariant-preserving transformations, disagreement preservation.

### Concurrency and distributed verification
Memory models, happens-before, linearizability, schedulers, clocks, partitions, quorum assumptions, retry/idempotency, crash/persistence semantics.

### Fault injection and recovery verification
Process/machine/network/storage/dependency faults, corruption, replay, resource exhaustion, recovery-time/durability invariants.

### Verification science
Mutation testing, coverage semantics, reproducibility, statistical uncertainty, tool evaluation, benchmark design, threats to validity.

## Standing authority nucleus

See [`../sources/REGISTRY.yaml`](../sources/REGISTRY.yaml). The nucleus includes primary tooling documentation and foundational research for property testing, fuzzing, sanitizers, static analysis, model checking, deductive verification, theorem proving, and formal modeling.

## Conversion pipeline

```text
SOURCE → proposition → property/specification → assumptions/trusted base
      → method/configuration → adversarial challenge → result/counterexample
      → reproducible receipt → refinement/transfer analysis
      → retained regression → teaching artifact → frontier question
```

Scaffold ≠ mastery. A source is not mastered until its mechanism can be reproduced, challenged, interpreted correctly, and transferred without overstating the evidence.
