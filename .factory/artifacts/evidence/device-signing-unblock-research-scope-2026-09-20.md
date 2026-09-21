# Device Signing Unblock Research Scope

Date cutoff: 2026-09-20 (inclusive)

## Audience

The founder/customer-zero decision maker and the factory operator responsible
for the meow-capture physical-device evidence lane.

## Jurisdiction

Apple-platform development on macOS/Xcode for locally paired iPhone/iPad
devices. This is an engineering and authorization decision, not legal advice.

## Decision to inform

Can the physical-device blocker be safely unblocked now, and if so, what is the
smallest authorized action? If not, what evidence can proceed without signing?

## Source plan

1. Local primary evidence: exact Xcode/build/device outputs, project settings,
   acceptance contract, and existing blocker records.
2. External primary evidence: Apple Developer/Xcode documentation on device
   testing, signing, provisioning, and Personal Team limits.
3. Secondary sources only to explain implementation implications, never to
   establish Apple policy when primary documentation is available.
4. Search each material claim and its strongest counterclaim; verify the source
   page directly and record retrieval date.

## Stopping rule

Stop when the decision-relevant claims are supported by direct local evidence
and official Apple documentation, and the remaining action is either a bounded
local change or an explicit human authorization gate. Do not attempt account
creation, provisioning updates, device installation, publication, or release.

## Known facts

- CoreDevice recognizes paired physical devices.
- The experiment build failed for lack of an authenticated account for the
  selected team and a matching provisioning profile.
- The product contract requires physical-device evidence for permission,
  route, microphone, playback, and interruption behavior.
- Simulator and Mac replay are explicitly insufficient for those claims.

## Open questions

- Can a Personal Team or a different authorized development team sign this
  local experiment without changing the product contract?
- Does Apple permit the required microphone/device behavior under that path?
- Which preflight can detect signing readiness before another device attempt?

## Hypotheses

- The blocker is authorization/provisioning, not device discovery or app logic.
- A team/profile change cannot be made autonomously under the repository’s
  governance boundary.
- Simulator and host work can proceed, but cannot close the physical-device
  acceptance claims.

## Provisional recommendation

Do not bypass signing or claim the device gate passed. Complete the portable
core and simulator/preflight work locally; request one explicit owner-authorized
development-signing action only if the owner wants physical validation now.
