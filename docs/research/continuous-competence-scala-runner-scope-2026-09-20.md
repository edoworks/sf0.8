# Scala Runner Research Scope

## Scope and cutoff

- Audience: the experiment owner deciding whether this local iPhone/iPad and mobile-web learning instrument should add executable coding exercises.
- Jurisdiction: technical product and platform feasibility only; no legal, educational-effectiveness, or App Store approval conclusion.
- Decision: choose an honest implementation boundary for Scala support and HackerRank/LeetCode-like test-case execution without weakening the experiment's local-only and dependency-free constraints.
- Date cutoff: 2026-09-20. Sources retrieved after this date are out of scope.
- Source plan: primary sources first: official Scala/Scala CLI documentation, browser/WebAssembly or JavaScript execution documentation, and official platform/security documentation. Use product pages or independent technical sources only to identify counterclaims or implementation patterns. Verify every material claim against the opened source.
- Stopping rule: stop when the decision-relevant claims are supported by at least one direct primary source and the strongest feasibility and safety counterclaims have been checked, or when the remaining question requires an empirical prototype.

## Known facts

- The current experiment is local-only and dependency-free.
- The mobile web surface has no code editor or test-case execution.
- The iOS surface has a static task bank and local session persistence, but no code execution.

## Open questions

- Can Scala code compile or execute locally in the current browser and iOS constraints without shipping a substantial runtime or network dependency?
- What minimum test-case model provides useful HackerRank/LeetCode-like feedback without executing arbitrary untrusted code?
- Should the first increment target a constrained, predeclared exercise runner rather than a general-purpose compiler?

## Hypotheses

- A general Scala compiler in the existing mobile-web artifact is not a small, dependency-free change.
- A constrained runner can provide real test-case evaluation for a narrow exercise while preserving local execution and an explicit safety boundary.

## Recommendations pending evidence

- Do not claim general Scala execution until a prototype compiles and runs representative submissions on the supported targets.
- Prefer a versioned exercise schema with visible test cases, hidden checks, expected outputs, and explicit language/runtime capability labels.
