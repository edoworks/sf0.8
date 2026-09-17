# Verification Recurrence: CoreSimulator Launch Failure

## Evidence

On 2026-09-14, the required `./scripts/doctor.sh && ./scripts/verify.sh`
check passed policy and formatting checks, then failed during XCTest launch with
`NSMachErrorDomain -308`; the simulator service hub died and the command timed
out. CI run `34902547551` completed successfully, so this is local simulator
infrastructure evidence rather than a product-test failure.

## 5-Whys

1. Why did local verification not complete? XCTest could not launch its
   simulator test worker.
2. Why could the worker not launch? CoreSimulator reported Mach error `-308`
   and a dead service hub.
3. Why was the service hub unavailable? The local simulator daemon state was
   stale or unhealthy; the deeper environment cause is unproven.
4. Why did the run encounter that state? The default local verification path
   does not pre-boot the destination (`BOOT_SIM=0`).
5. Why is pre-boot disabled locally? The script defaults to a conservative
   local run and leaves CI's faster, warmed-up path opt-in.

## Correction and Guard

- Immediate correction: rerun with `BOOT_SIM=1 CLEAN=0` after simulator service
  recovery; do not claim a green gate from the failed run.
- Root-cause correction: keep destination pre-boot available as the documented
  recovery path and consider making it the local default if this recurrence is
  observed again.
- Mechanical guard: `verify.sh` pre-boots the named destination when
  `BOOT_SIM=1`; the rerun must produce a fresh result bundle and passing test
  summary before verification is considered complete.

The deeper cause of the simulator daemon failure remains an assumption pending
additional environment evidence.

Follow-up evidence: the same `-308` failure recurred during the first full
working-tree verification on 2026-09-15. Shutting down all simulator devices
and restarting `com.apple.CoreSimulator.CoreSimulatorService` restored the
daemon; the full suite then passed. This confirms the recovery guard is
effective but also confirms the local daemon issue is recurring.

Additional evidence: the first verification attempt for the simplicity and
hierarchy increment again reached the build/test launch phase and timed out
with repeated LLDB snapshot errors and `-308`. A direct boot and boot-status
check for the existing iPhone 17 Pro destination restored a usable simulator;
the subsequent `BOOT_SIM=1 CLEAN=0 ./scripts/verify.sh` completed with the full
suite green. This remains local infrastructure evidence, not a product-test
failure.
