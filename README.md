# Genius-Verification

[![Buildkite](https://badge.buildkite.com/7584c53dee7ea5a56fb7285cc4c67007fc275bfd5d7598222f.svg)](https://buildkite.com/casey-1/genius-verification)

Domain repository for **verification mastery**.

Identity: `Genius-Verification` only (hyphenated; no colon-form dual identity).

## Scope

- Specification and oracle design
- Property-based and model-based testing
- Coverage-guided and structure-aware fuzzing
- Sanitizers (ASan, UBSan, TSan, MSan, …)
- Static analysis / CodeQL-class tooling
- Differential and metamorphic testing
- Model checking & formal specification (TLA+, Alloy, …)
- Deductive verification (Dafny-class)
- Interactive theorem proving (Lean-class)
- Fault injection and recovery verification
- Evidence discipline: every material verification run can emit a durable receipt

## Epistemic foundation

[`mastery/EPISTEMOLOGY.md`](mastery/EPISTEMOLOGY.md) defines the domain law:

> Verification never proves more than the specification, model, oracle, explored state space, and execution environment actually support.

Every material result is interpreted as:

```text
SYSTEM + PROPERTY + ASSUMPTIONS + MODEL + EVIDENCE → JUSTIFIED CLAIM
```

This keeps testing, fuzzing, static analysis, model checking, deductive proof, theorem proving, fault injection, and production observation distinct while allowing them to compound as independent evidence.

## Authority nucleus

[`sources/REGISTRY.yaml`](sources/REGISTRY.yaml) contains primary and foundational sources spanning QuickCheck/property testing, LLVM fuzzing/sanitizers, CodeQL, Lamport/TLA+, Alloy, Dafny, Lean, and supporting formal-verification material.

## Doctrine

Scaffold ≠ mastery. Claims stay `mapped` until evidence receipts exist.

A PASS must preserve the proposition checked, assumptions, oracle/model, tool/configuration, source SHA, relevant state-space limits, artifacts, counterexamples, and transfer limits. Green UI alone is not terminal proof.

Composes with:

- [Genius-Mastery](https://github.com/GlacierEQ/Genius-Mastery) — schemas, validator, family protocol
- [Genius-Code](https://github.com/GlacierEQ/Genius-Code) — first consumer of property-testing capability

## Status (truthful)

| Surface | State |
|---------|-------|
| GENIUS.yaml v2 | Implemented |
| Mastery map / vector / retention | Seed + doctoral epistemology |
| Claims | Mapped examples only |
| Sources | Expanded primary/foundational verification nucleus |
| Challenge ladder | Skeleton |
| Evidence ledger | Empty |
| Model-checking / fuzzer harnesses | Not yet populated |
| Buildkite CI (`casey-1/genius-verification`) | Observed PASS on [build #1](https://buildkite.com/casey-1/genius-verification/builds/1) @ `8ff682260a36f42b953f146622488fd557cc20f3` |

## License

MIT — see LICENSE.
