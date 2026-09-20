# Issue-Binding Red-Team 5-Whys

## Finding

The first implementation attempted the write probe before validating the issue
repository and canonical issue identity.

1. Why could an unrelated issue receive a probe? The issue number was accepted
   from the caller and the probe ran before binding validation.
2. Why was caller input trusted? The gate checked creation/reuse and identity,
   but had no trusted per-capability binding.
3. Why was there no binding? The issue capability was modeled as a generic
   lifecycle permission rather than a work-scoped capability.
4. Why did tests miss it? They covered missing issue and denied writes, but not
   an unrelated issue with a valid-looking URL.

Evidence ends here; no further cause is established without the original
permission-design decision record.

## Correction

- Immediate: validate canonical marker, repository, URL shape, and expected
  issue before identity or any GitHub write.
- Root cause: add `.factory/control-plane-bindings.json` and require the
  material entrypoint to resolve the expected issue from that factory record.
- Recurrence guard: adversarial unit tests and deny-by-default issue/PR/repo
  permission patterns cover unrelated issue and unrelated GitHub writes.
