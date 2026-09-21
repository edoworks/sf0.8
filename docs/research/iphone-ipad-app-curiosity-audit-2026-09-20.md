# iPhone/iPad App Delivery Curiosity Audit

Date: 2026-09-20  
Decision context: whether the continuous-competence experiment should proceed
directly to native iPhone/iPad implementation  
Audience: founder/operator  
Jurisdiction: Apple-platform product development; no release or purchase decision
is authorized by this review  
Cutoff: 2026-09-20

## Strongest Charitable Restatement

The claim is not that every iOS project is trivial. Its strongest defensible
form is:

> Building a narrow, local-first iPhone/iPad app with ordinary SwiftUI/Xcode
> patterns is a well-understood and comparatively inexpensive engineering task.
> Existing knowledge, prior Apple work, and the current mobile experiment should
> make native implementation a feasible next step rather than a presumed blocker.

That claim is substantially right. It does not establish that native delivery is
the cheapest way to learn whether this particular intervention works, that an App
Store release is warranted, or that native features will improve retention.

## Evidence, Inference, Unknowns

| Status | Claim | Evidence | Limitation |
|---|---|---|---|
| Evidence | The repository has prior iOS/iPadOS delivery knowledge. | The Apple capability registry records iOS and iPadOS build/package paths, prior Product A archive evidence, and required device-family evidence in `.factory/apple-distribution/capabilities.json`. | The registry marks these capabilities `SUPPORTED_UNVERIFIED`; it is not proof of current release readiness. |
| Evidence | A phone/iPad experiment already exists without native dependencies. | `experiments/continuous-competence-mobile/` provides responsive UI, local storage, export, and an offline-capable installable web shell. | It has not yet supplied participant, retention, or comparative learning evidence. |
| Evidence | Apple development and testing have a standard toolchain. | Apple documentation identifies SwiftUI, Xcode, device archives, TestFlight, and App Review as established platform paths. See the source list below. | Standard tooling does not remove device coverage, privacy, accessibility, metadata, signing, or review work. |
| Inference | Native implementation is technically feasible at low marginal engineering cost for this narrow scope. | The feature is local-first, accountless, model-free, and deterministic; these avoid the most expensive backend and integration surfaces. | Cost depends on the actual target, device access, polish bar, and whether notifications, audio, camera, sync, or payments are added. |
| Inference | Native implementation is not yet the highest-information next step. | The experiment can test the intervention and phone/iPad friction now using the existing surface. | This changes if the web surface causes a measured failure attributable to a missing OS capability. |
| Unknown | Whether native improves completion, resumption, or repeat use. | No external participant or comparative surface evidence exists. | Requires a paired surface test with the same task and instrument. |
| Unknown | Whether there is a market, buyer, or acceptable App Store economics. | No payment, repeat-use, or distribution evidence exists. | Technical feasibility cannot answer these questions. |

## Existing iOS/iPadOS Knowledge Applied

For this experiment, the known low-cost path is:

- Keep the learning protocol and fixtures independent of the UI and model.
- Start with a local-first, accountless implementation and synthetic content.
- Use SwiftUI for a shared iPhone/iPad presentation, with adaptive layouts rather
  than separate feature branches.
- Preserve independent-performance measurement separately from assisted work.
- Add OS capabilities only behind explicit evidence: notifications for return
  behavior, offline persistence for interruption recovery, voice for input burden,
  or camera/system integration for a measured workflow need.
- Validate on both phone and iPad, including interruption, rotation/size changes,
  accessibility, persistence, export, and privacy behavior.
- Treat TestFlight/App Review as a later human-gated distribution path, not as
  evidence that the experiment works.

This is sufficient knowledge to proceed with a native spike if the owner wants
to test the surface. It is not a reason to replace the current experiment before
the current surface has been exercised.

## High-Value Questions

1. What exact failure in the current mobile web/static flow cannot be fixed more
   cheaply in that flow?
2. Does the target user need a device capability, or merely a reliable mobile
   entry point and resumable state?
3. Will native delivery measure the learning intervention, or introduce novelty,
   onboarding, and notification effects that confound the result?
4. Is the intended scope still local-only and adult-only, or are accounts,
   cloud sync, child use, audio, camera, or payments being contemplated?
5. What is the minimum owner-approved evidence required before TestFlight or App
   Store distribution is worth its metadata, privacy, signing, and review cost?

## Counterevidence and Failure Modes

- A native app may increase friction through install, permissions, updates, and
  TestFlight management even if the code is inexpensive.
- A responsive web app may be sufficient, making native work an opportunity-cost
  failure rather than an engineering failure.
- Notifications can increase prompted completion without increasing voluntary
  repeat use or independent competence.
- Offline support can preserve access while silently complicating result export,
  recovery, and data integrity.
- iPhone and iPad are not one visual target: a shared codebase still needs
  device-family layout and accessibility evidence.
- App Store approval, monetization, privacy declarations, and public release are
  separate human decisions and are not implied by a successful local build.

## Falsifiable Test

Run a small, owner-authorized paired-surface self-pass before committing to a
native build:

1. Complete five predeclared sessions in the existing mobile web/static flow.
2. Record completion, interruption/resumption, useful-progress latency, export
   reliability, and whether a missing OS capability caused abandonment.
3. If a concrete device-specific failure occurs, implement only the smallest
   native SwiftUI spike that addresses it and repeat the same five-session
   protocol on iPhone and iPad.
4. Compare the surfaces on completion, independent score, transfer score,
   resumption, unprompted return, and surface-caused errors.

Native proceeds only if the device-specific capability improves a predeclared
outcome without weakening independent-performance measurement. Otherwise retain
the mobile web/static artifact and do not build a native product surface.

## Recommendation

**Confidence: high** that narrow iPhone/iPad construction is technically feasible
and that the repository has sufficient existing knowledge to avoid treating it as
an engineering blocker.

**Confidence: medium** that a native prototype is worth doing now. The evidence
supports proceeding with the Customer Zero experiment, not automatically
proceeding with native implementation.

Proceed with the existing mobile experiment first. Keep a native SwiftUI spike as
an explicitly bounded follow-up, triggered by observed device-specific friction.
This confirms the user's premise in the engineering sense while preserving the
cheaper and more discriminating validation path.

## What Would Change This Recommendation

Proceed directly to native if the owner decides that one of these is a required
research variable and authorizes it: reliable background/notification behavior,
offline operation that the web surface cannot provide, voice/camera input,
system integration, or a controlled comparison showing materially better
completion or repeat use.

Defer native if the current surface completes the task, if the difference is only
branding or polish, if native work adds accounts/cloud/model dependencies, or if
the intervention has no delayed independent-performance advantage.

## Conclusion Revision

Initial intuition: “iPhone/iPad app construction should not be an issue.”

Revised conclusion: **correct as a feasibility claim; too broad as a sequencing
claim**. The technical path is known and affordable for this narrow scope. The
remaining uncertainty is product evidence and whether native capabilities change
the measured outcome.

## Human Gate

This audit authorizes no recruitment, external outreach, purchase, publication,
TestFlight submission, App Store submission, or release. A human must choose the
surface, approve any native spike, and review privacy, accessibility, device, and
distribution evidence before external testing.

## Sources

### Primary

- Apple Developer, SwiftUI documentation, https://developer.apple.com/documentation/swiftui.md,
  retrieved 2026-09-20.
- Apple Developer, TestFlight, https://developer.apple.com/testflight/, retrieved
  2026-09-20.
- Apple Developer, App Review Guidelines,
  https://developer.apple.com/app-store/review/guidelines/, retrieved 2026-09-20.
- Repository capability registry, `.factory/apple-distribution/capabilities.json`,
  verified 2026-09-18.

### Local implementation evidence

- `experiments/continuous-competence-mobile/README.md`.
- `docs/research/continuous-human-competence-artifact-decomposition-2026-09-20.md`.
- `docs/apple-distribution-workflow.md`.
- `docs/apple-distribution-capabilities.md`.

### Unresolved

- No source here proves current App Review approval, external TestFlight success,
  user retention, willingness to pay, or a native-vs-web outcome difference.
