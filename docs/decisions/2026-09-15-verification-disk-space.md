# Verification Blocker: Host Disk Space

## Evidence

The first verification run for the design-validation increment passed the
toolchain, policy, cleanup, and formatting stages but was blocked by the
5 GiB preflight with 5,097,812 KiB available. After the simulator recovery and
one successful verification using the documented `MIN_FREE_GIB=4` override,
the next verification attempt found 2,446,976 KiB available and stopped before
Xcode work. The project filesystem is 100% full according to `df -h`.

## 5-Whys

1. Why did verification stop? The disk-space preflight rejected the run.
2. Why did it reject the run? Available space was below both the normal 5 GiB
   threshold and the temporary 4 GiB override.
3. Why is available space low? The host filesystem has only about 2.3 GiB
   free; the cause of the broader host usage is not established by the
   evidence collected here.

The analysis stops because no evidence identifies which unrelated data is safe
to remove. Assumptions about DerivedData or other caches are not treated as
root cause.

## Correction and Guard

- Immediate correction: restore host free space above 5 GiB before rerunning
  `./scripts/verify.sh`; do not lower the guard further.
- Root-cause correction: identify and approve safe host cleanup outside the
  repository before the next Xcode verification session.
- Mechanical guard: `scripts/check-disk-space.sh` blocks verification before
  Xcode work when the configured minimum is unavailable.

Additional evidence: a verification run with parallel testing explicitly
disabled still consumed approximately 2.4 GiB during the single-destination
XCTest launch and ended with CoreSimulator `-308`; no `Clone 1`, `Clone 2`, or
`Clone 3` destinations were created. The host ended with approximately 2.6 GiB
free. This separates test-clone multiplication from the remaining disk and
CoreSimulator failure modes; more headroom is required before another full run.
