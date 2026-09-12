# Genius-Verification Epistemology

## Purpose

Verification is the discipline of reducing justified uncertainty about whether a system satisfies a stated property under explicit assumptions. It is not synonymous with testing, formal proof, CI success, code coverage, or the absence of observed failures.

The central object is always a proposition:

```text
SYSTEM + PROPERTY + ASSUMPTIONS + MODEL + EVIDENCE → JUSTIFIED CLAIM
```

A verification result is meaningful only when all five components are explicit enough to inspect and challenge.

## Prime law

> Verification never proves more than the specification, model, oracle, explored state space, and execution environment actually support.

A perfect proof of the wrong specification is still wrong. A million passing tests with a weak oracle establish little. A model checker can exhaustively explore only the model and bounds supplied to it. A sanitizer detects particular runtime violations only on executions that reach them. Static analyses trade soundness, completeness, and precision. Production telemetry observes deployed behavior but does not enumerate unobserved executions.

The verification loop is therefore:

```text
SPECIFY → MODEL → GENERATE/EXPLORE → OBSERVE → CHECK → CHALLENGE
       → MINIMIZE COUNTEREXAMPLE → REPRODUCE → PRESERVE RECEIPT → REVISE
```

## 1. Verification propositions

Before choosing a method, classify the proposition.

### Safety
"Something bad never happens."

Examples: no double-spend, no use-after-free, no privilege escalation, no two leaders committed for the same term under the modeled protocol.

Safety violations are witnessed by finite counterexamples.

### Liveness
"Something good eventually happens."

Examples: requests eventually complete, elections eventually produce a leader, a lock request is eventually served.

Liveness depends critically on fairness and timing assumptions. A safety proof does not imply liveness.

### Functional correctness
Implementation outputs and state transitions satisfy preconditions, postconditions, invariants, and refinement relations.

### Memory and undefined-behavior freedom
No prohibited memory, race, initialization, alignment, lifetime, or language-level undefined behaviors occur under the checked conditions.

### Security
A stated adversary cannot violate confidentiality, integrity, authenticity, authorization, isolation, or another security property under explicit cryptographic and trust assumptions.

### Reliability and recovery
The system preserves required properties across crashes, restarts, partial writes, retries, corruption, partitions, resource exhaustion, and restoration.

### Performance envelopes
Latency, throughput, resource use, or scalability remain within declared bounds for defined workloads and environments.

Performance verification is empirical unless the claim is purely analytic; distributions, tails, and uncertainty matter.

## 2. Specification adequacy comes before proof strength

Verification cannot rescue an incomplete requirement.

For every material property, ask:

- What behavior is required?
- What behavior is forbidden?
- What states and transitions exist?
- What environmental assumptions are allowed?
- Which actors are adversarial or faulty?
- What observations count as externally visible?
- What is intentionally left unspecified?

A specification should be challenged with the same aggression as an implementation. Vacuous truth, contradictory assumptions, missing environment behavior, and overconstrained models can all create false confidence.

## 3. Oracles define what tests can know

A test input without a trustworthy oracle is only an execution.

Oracle forms include:

- exact expected outputs;
- executable reference models;
- algebraic properties and invariants;
- metamorphic relations;
- differential comparison against independent implementations;
- protocol/state-machine predicates;
- runtime assertions;
- proof obligations.

Oracle weakness is a first-class risk. If two implementations share the same defect or specification misunderstanding, differential agreement can still be wrong.

## 4. Example testing is local evidence

Unit and integration tests are valuable for regressions, boundaries, and known behaviors. Their epistemic limit is selection: humans choose examples, usually from understood cases.

A passing example test establishes only that the checked path, data, environment, and oracle agreed for that execution.

Use examples for named cases; do not generalize them into universal claims without additional evidence.

## 5. Property-based testing searches classes, not anecdotes

Property-based testing turns expected behavior into general predicates and generates many inputs intended to challenge those predicates.

Strong practice requires:

```text
PROPERTY → GENERATOR → DISTRIBUTION → EXECUTION → ORACLE
         → SHRINKER → MINIMAL COUNTEREXAMPLE → REGRESSION
```

Evaluate generator reachability and distribution, not just test count. A property never exercised near its difficult boundary can be technically green and practically weak.

Shrinking is epistemically important: the minimal counterexample improves causal understanding and creates a durable regression artifact.

## 6. Fuzzing is adversarial state-space sampling

Coverage-guided fuzzing biases generation toward executions that reveal new program behavior. Structure-aware and grammar-aware fuzzing improve reachability for constrained inputs such as protocols, parsers, file formats, and APIs.

A fuzzer PASS does not mean absence of bugs. Record:

- corpus and seed provenance;
- target/harness;
- coverage signal;
- sanitizer configuration;
- duration and execution count;
- dictionary/grammar;
- platform/compiler/build flags;
- crashes, hangs, and minimized reproducers.

Fuzzing becomes stronger when combined with sanitizers, differential oracles, assertions, and stateful models.

## 7. Sanitizers are dynamic detectors, not proofs

Sanitizers instrument execution to detect defined classes of runtime violations.

Examples:

- ASan: memory safety violations such as out-of-bounds and use-after-free;
- TSan: data races under observed executions;
- MSan: uses of uninitialized memory;
- UBSan: selected undefined behaviors.

Their evidence is path-dependent. No finding means no detector-triggering violation was observed on the executions run with that instrumentation.

Detector configuration, optimization level, compiler, suppression rules, and platform belong in the receipt.

## 8. Static analysis is an abstraction with tradeoffs

Static analyses approximate program behavior without executing every concrete path.

Three dimensions must remain explicit:

- **soundness** — whether relevant concrete behaviors can be missed;
- **completeness** — whether every reported issue corresponds to a real violation;
- **precision** — how closely the abstraction distinguishes concrete states.

In real tools, these are often property- and configuration-specific rather than absolute labels.

False positives, false negatives, unsupported language features, library models, path sensitivity, alias approximations, and interprocedural limits belong in the interpretation of results.

## 9. Differential testing requires independence

Differential testing compares outputs or behaviors across implementations, versions, compilers, configurations, or models.

Its force comes from independent failure modes. Shared code, shared libraries, copied algorithms, identical compilers, or the same incorrect standard interpretation reduce independence.

When disagreement occurs, preserve the input and all competing outputs before deciding which implementation is wrong.

## 10. Model checking verifies a finite semantic model

A model checker explores reachable states of a formal model and checks stated properties. This can provide exhaustive evidence for the modeled state space.

The proof burden includes:

- fidelity of the model to the intended system;
- initial states;
- transition relation;
- invariants and temporal properties;
- fairness assumptions;
- state bounds and symmetry reductions;
- abstraction choices;
- environment behavior.

A model-checking result should state whether it is exhaustive over the model, bounded, sampled, symmetry-reduced, or otherwise constrained.

Counterexample traces are first-class outputs and should become implementation tests where transfer is possible.

## 11. Formal proof is proof relative to foundations and assumptions

A mechanized proof establishes a proposition in a formal system, checked by a kernel or verifier. Its strength depends on:

- the theorem statement;
- formal definitions;
- axioms and trusted base;
- specification fidelity;
- compiler/extraction/refinement assumptions when executable code is involved.

Keep separate:

```text
proof of model property
proof of algorithm
proof of source program
proof of compiler/refinement
proof about deployed binary/runtime
```

They are connected obligations, not synonyms.

Small trusted kernels, proof-term checking, independent checking, and reproducible builds reduce the trusted computing base.

## 12. Refinement bridges abstraction levels

High-level models are useful only if there is a justified relation to lower-level artifacts.

Use refinement questions:

- Does every implementation transition correspond to an allowed abstract transition?
- Are externally visible behaviors preserved?
- Which implementation details are hidden by abstraction?
- Which new failure modes appear below the model?
- Is the refinement argument tested, proved, or assumed?

The larger the semantic gap, the weaker the transfer from formal result to production claim unless additional evidence closes it.

## 13. Concurrency and distributed verification require explicit adversaries

For concurrent and distributed systems, specify:

- event ordering and happens-before;
- atomicity and linearization points where applicable;
- memory model;
- scheduler/fairness model;
- crash, omission, partition, corruption, and Byzantine assumptions;
- retry and idempotency semantics;
- clocks and timeouts;
- quorum and membership behavior;
- persistence boundaries.

Deterministic sequential tests are weak evidence for these properties unless the concurrency/failure dimensions are deliberately controlled or explored.

## 14. Fault injection verifies recovery claims

Fault injection is verification only when a property and oracle are defined.

Injectable dimensions include:

- process crash;
- machine loss;
- network partition/delay/drop/reordering;
- disk full / I/O error / partial write;
- dependency timeout;
- malformed or stale data;
- clock skew;
- resource exhaustion;
- duplicate delivery;
- restart and replay.

The important result is not "the chaos test ran." It is whether the required invariant, recovery time, durability boundary, and observable behavior survived the declared fault.

## 15. Coverage is a diagnostic, not a correctness metric

Line, branch, path, mutation, state, requirement, and specification coverage answer different questions.

High line coverage can coexist with weak assertions. Low mutation survival can reveal oracle weakness. Model-state coverage can reveal unreachable assumptions. Requirement coverage can expose untested obligations.

Never turn a coverage percentage into a correctness probability without a defensible statistical model.

## 16. Counterexamples outrank confidence narratives

One valid counterexample falsifies a universal claim.

Counterexamples should be:

1. preserved immediately;
2. minimized where possible;
3. reproduced independently;
4. classified against the specification;
5. converted into a regression or proof obligation;
6. linked to the corrected claim and fix;
7. retained even after resolution.

Do not delete inconvenient evidence from the knowledge system.

## 17. Reproducibility is part of the result

A verification receipt should bind at least:

```text
claim_id
source/revision/SHA
specification/property version
tool + version
command/configuration
compiler/runtime/dependencies
platform/environment
seed/corpus/model bounds
start/end time
exit status
stdout/stderr or structured result
artifact hashes
counterexamples/reproducers
interpretation and limits
```

A screenshot or green badge is useful routing evidence but weaker than a machine-readable, SHA-bound receipt with artifacts.

## 18. Evidence independence raises confidence

Repeated execution of one test suite is not equivalent to independent verification.

Confidence compounds more strongly when different failure mechanisms agree:

```text
spec review
+ example tests
+ property tests
+ fuzzing
+ sanitizer instrumentation
+ static analysis
+ model checking
+ proof where justified
+ fault injection
+ production observability
```

The goal is not maximum tool count. It is orthogonal evidence against the highest-consequence uncertainty.

## 19. Verification debt

Verification debt accumulates when:

- properties are implicit;
- oracles are weak;
- flaky tests are ignored;
- suppressions grow without review;
- fuzz corpora stagnate;
- models diverge from implementations;
- proof assumptions become stale;
- tool versions drift;
- receipts are missing;
- counterexamples are fixed without retention.

Track these as state, not folklore.

## 20. Doctoral verification posture

For any nontrivial system, a verification researcher should be able to:

1. define the proposition precisely;
2. identify the smallest adequate semantic model;
3. state the trusted computing base;
4. choose evidence methods whose strengths match the risk;
5. construct adversarial inputs and environments;
6. distinguish exhaustive from sampled evidence;
7. explain soundness, completeness, and precision limits;
8. preserve counterexamples and negative results;
9. connect abstract verification to implementation through refinement;
10. reproduce the result from source and configuration;
11. state exactly what remains unverified.

## 21. Foundational corpus

The standing verification corpus includes:

- QuickCheck and modern property-based testing;
- LLVM libFuzzer and sanitizers;
- static program analysis and abstract interpretation;
- Leslie Lamport's TLA+ materials and *A Science of Concurrent Programs*;
- Alloy and bounded relational/temporal model finding;
- Dafny and automated deductive program verification;
- Lean and small-kernel interactive theorem proving;
- model checking foundations;
- differential testing and compiler validation;
- fault injection and systems-recovery testing.

Sources belong in `sources/REGISTRY.yaml`; this document records the epistemic contract they support.

## Conversion contract

Every important verification source should eventually become executable knowledge:

```text
SOURCE
  → proposition class
  → formal or executable property
  → assumptions / trusted base
  → method + configuration
  → adversarial challenge
  → counterexample or PASS artifact
  → reproducible receipt
  → transfer/refinement analysis
  → retained regression
  → frontier question
```

## Final rule

> Never ask only whether verification passed. Ask what exact proposition was checked, against which model and assumptions, with what oracle or proof system, over what state space or executions, what the trusted base was, what counterexample would falsify the claim, and whether the evidence transfers to the artifact that will actually run.
