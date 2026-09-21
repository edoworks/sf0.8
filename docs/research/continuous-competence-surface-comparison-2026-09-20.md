# Customer-Zero Surface Comparison

Status: `BLOCKED_WAITING_SIGNING_AUTHORIZATION`
Bound issue: #50
Population: founder Customer Zero, adult software engineer and parent
Scope: compare delivery surfaces, not market demand or learning effectiveness

## Purpose

Determine whether native iPhone/iPad delivery changes the ability to complete
and resume the same competence session compared with the existing mobile web
surface. The native app and web flow use the same task and control/intervention
contract.

## Surfaces

1. Mobile web/PWA: `experiments/continuous-competence-mobile/`
2. Native SwiftUI: `experiments/continuous-competence-ios/`

Do not compare different content, task difficulty, prompts, or time limits.

## Five-session protocol

Run five sessions on each surface, alternating surface order where practical.
Use the same mode sequence on both surfaces:

| Session | Mode |
|---:|---|
| 1 | CONTROL |
| 2 | INTERVENTION |
| 3 | CONTROL |
| 4 | INTERVENTION |
| 5 | INTERVENTION |

Each session is limited to 10 minutes. Use only synthetic or non-confidential
material. Do not include child data.

## Record per session

- surface: `WEB` or `NATIVE_IOS_IPADOS`;
- device: phone, iPad, or desktop fallback;
- mode: `CONTROL` or `INTERVENTION`;
- started without a reminder: yes/no;
- time to useful progress;
- completed: yes/no;
- interruption and resumption success;
- context that had to be re-entered;
- independent answer and confidence;
- defect detection and repair, when intervention;
- export success;
- surface-caused error or friction;
- would use again without prompting: yes/no;
- notes on voice, notification, offline, or system integration need.

## Decision thresholds

Native delivery earns a follow-up only if:

- it completes at least as reliably as web;
- it produces a concrete device-specific improvement in resumption, input,
  offline use, or repeat behavior;
- the improvement is not merely novelty or prompting;
- independent-performance measurement remains equivalent;
- no account, cloud, model, child, payment, or release dependency is needed.

Otherwise retain the web/PWA artifact and do not expand native scope.

## Human gate

The founder must run the sessions on an approved physical device or explicitly
authorize a private local delivery path. Simulator screenshots establish layout
feasibility only; they are not Customer Zero behavior evidence.

Current environment check on 2026-09-20: no physical iPhone or iPad is
connected to `xctrace`, but CoreDevice and Xcode recognize physical targets.
`xcrun devicectl list devices` reports Ethan, helloMax, and supportXR as
`available (paired)`, and `xcodebuild -showdestinations` lists all three as
iOS destinations. The old `xctrace` check was therefore incorrect. Use
`python3 scripts/check-apple-device.py --device Ethan` as the availability gate.

The next physical-device attempt is blocked by development signing: the target
has no configured development team or provisioning profile for its bundle
identifier. The Mac has a valid Apple Development identity, but using automatic
provisioning failed because Xcode has no authenticated account for team
`YM5MWC8YJF`. Adding an account/profile requires human authorization. No device
installation, LAN exposure, TestFlight submission, or public hosting was
attempted.
