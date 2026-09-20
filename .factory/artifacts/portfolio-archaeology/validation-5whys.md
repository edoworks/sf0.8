# Validation Failure 5-Whys

## Symptom

The focused pytest command failed during collection with
`ModuleNotFoundError: No module named 'scripts'` in

## Analysis

1. Why did collection fail? The test imported `scripts.ecosystem_gates`, but
   Python did not recognize `scripts` as an importable package in this test
   invocation.
2. Why was it not recognized? The repository had no `scripts/__init__.py`.
3. Why was that material? The test suite uses package imports rather than
   loading the module by file path.
4. Why was the mismatch not caught earlier? Existing validation commands run
   scripts directly and did not exercise this collection path.
5. Why is recurrence possible? Package-boundary assumptions were implicit and
   lacked a mechanical import smoke test.

## Correction

- Immediate: add the minimal `scripts/__init__.py` package marker.
- Root cause: make package importability part of focused verification; retain
  the test module's import path as a guard.

## Evidence

The focused pytest command is rerun after the correction. No destructive or
external action was involved.
