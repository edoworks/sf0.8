# Scala Test-Case Runner Deep Dive

## Scope and cutoff

Audience: experiment owner. Jurisdiction: technical feasibility only. Decision:
how to add Scala support and HackerRank/LeetCode-like test cases while keeping
the artifact local-only and dependency-free. Cutoff: 2026-09-20. The source
plan and stopping rule are recorded in
`continuous-competence-scala-runner-scope-2026-09-20.md`.

## Executive answer

- **High confidence:** Scala has mature compile/run/test tooling. Scala CLI's
  official overview explicitly lists compilation, execution, packaging, REPL,
  and test-suite support across Scala 3.x, 2.13.x, and 2.12.x. [P1, retrieved
  2026-09-20]
- **High confidence:** A browser page can run Scala.js output, but the official
  tutorial requires a Scala.js build configured with sbt and a JDK/toolchain;
  it is not equivalent to compiling arbitrary Scala entered into this static
  page. [P2, retrieved 2026-09-20]
- **High confidence:** HackerRank's official walkthrough describes the relevant
  interaction contract: choose a language, enter code, compile/test for errors
  and accuracy, then submit for results. [P3, retrieved 2026-09-20]
- **Medium confidence:** The smallest honest increment for this experiment is
  a Scala exercise fixture plus a local, visible test-case harness, with an
  explicit limitation that it does not compile arbitrary Scala. A general
  compiler needs a separately built and versioned runtime or a trusted host
  execution service, both outside the current artifact constraints.

## Findings

### Claim 1: Scala support is feasible, but general compilation is a toolchain feature

**Evidence:** Scala CLI documents compile, run, package, REPL, and test commands,
and lists JVM as the default execution target plus Scala.js and Scala Native.
This establishes that real Scala test execution is available in a proper
toolchain. [P1, primary vendor documentation, retrieved 2026-09-20]

**Counterevidence:** The Scala.js tutorial requires JDK, sbt, a Scala.js plugin,
and Node.js for its complete flow, then generates JavaScript before the browser
loads it. [P2, primary project documentation, retrieved 2026-09-20]

**Implication:** Labeling a static browser harness as a Scala compiler would be
incorrect. This increment labels the fixture as Scala and executes its local
exercise contract instead.

### Claim 2: Test-case execution should expose examples, expected outputs, and pass/fail results

**Evidence:** HackerRank's official challenge walkthrough describes a problem
statement with sample input/output, language selection, code entry, compiling
and testing for accuracy, and result submission. [P3, primary product page,
retrieved 2026-09-20]

**Counterevidence:** The current experiment has no server, account, upload, or
external runtime, so hidden tests, arbitrary submission execution, resource
quotas, and compiler diagnostics cannot be claimed from this surface.

**Implication:** The implemented runner provides visible cases and pass/fail
output for the bundled contract. It is analogous to the test loop, not a
platform-grade judge.

### Claim 3: Scala.js is a possible future browser execution path but needs compatibility qualification

**Evidence:** Scala.js documentation states that it targets JavaScript and that
its semantics are generally Scala-like, while documenting differences such as
reflection support and undefined-behavior handling. [P4, primary project
documentation, retrieved 2026-09-20]

**Counterevidence:** A prebuilt Scala.js bundle would add build artifacts,
versioning, and a runtime surface; compiling user-submitted source in-browser
would still require a compiler and resource isolation. No source reviewed here
establishes that this repository already has that bundle or sandbox.

**Implication:** Defer general in-browser Scala execution until a prototype
proves bundle size, offline install, supported language subset, timeout/memory
behavior, and parity with intended JVM results.

## Known facts, open questions, hypotheses, recommendations

- Known facts: the artifact is dependency-free and local-only; before this
  increment it had no executable test-case UI; Scala CLI and Scala.js provide
  external evidence for real Scala execution workflows.
- Open questions: whether a bundled Scala.js runtime fits the mobile artifact;
  whether iOS should share the same runner; what resource limits are acceptable
  for user-authored code.
- Hypotheses: a constrained contract runner is useful for the current learning
  experiment; general compilation is a separate product capability.
- Recommendations: keep the limitation visible; version test cases; add hidden
  cases only when an actual judge/runtime exists; never execute arbitrary source
  without a separately reviewed isolation design.

## Conflicts and unknowns

- Scala CLI presents JVM, Scala.js, and Scala Native as supported targets, while
  the browser tutorial's prerequisites show that target support does not remove
  the need for a build toolchain. These are compatible claims, not a conflict.
- The requested “similar to HackerRank/LeetCode” scope is ambiguous between a
  test-case UX and arbitrary code judging. This implementation chooses the UX
  interpretation and records the boundary.
- No verified source in this pass established a safe, offline, arbitrary-Scala
  compiler for iOS Safari or a static iOS app. That remains an empirical and
  architecture question.

## Decision implications and what would change the conclusion

Proceed with the local contract runner for the experiment and do not call it a
general Scala runner. The conclusion would change if a prototype demonstrates a
reviewed Scala.js/JVM execution path with offline installation, bounded CPU and
memory, deterministic test results, and a clear policy for untrusted code.

## Sources

### Primary

- [P1] Scala CLI, “Overview,” official documentation: https://scala-cli.virtuslab.org/docs/overview/ (retrieved 2026-09-20).
- [P2] Scala.js, “Basic tutorial,” official project documentation: https://www.scala-js.org/doc/tutorial/basic/ (retrieved 2026-09-20).
- [P3] HackerRank, “Programming Problems and Competitions,” official product walkthrough: https://www.hackerrank.com/for-developers (retrieved 2026-09-20).
- [P4] Scala.js, “Semantics of Scala.js,” official project documentation: https://www.scala-js.org/doc/semantics.html (retrieved 2026-09-20).

### Secondary

- None used for material claims.

### Lead-only

- LeetCode Help Center URLs consulted for platform context returned unrelated or
  unavailable articles during retrieval and were not used as evidence.
