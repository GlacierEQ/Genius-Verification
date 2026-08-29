# Mastery Map — Genius-Verification

## Irreducible questions

1. What properties must hold for a class of inputs or interleavings?
2. Which verification method matches the risk and state space?
3. How do we turn a verification run into durable, inspectable evidence?
4. When does a passing suite *not* justify a claim (coverage gaps, oracle weakness, flaky environment)?
5. How do counterexamples become first-class evidence rather than noise?

## Method surfaces

| Method | Typical use |
|--------|-------------|
| Example / unit tests | Local behavior, regressions |
| Integration tests | Boundaries between components |
| Property-based tests | Broad input spaces + invariants |
| Fuzzing | Parsers, protocols, adversarial surfaces |
| Sanitizers | Memory, races, UB |
| Static analysis | CodeQL-class, language analyzers |
| Differential testing | Independent implementations / versions |
| Model checking / formal | Concurrency, protocols, safety properties |
| Fault injection | Timeouts, partitions, corruption, restarts |
