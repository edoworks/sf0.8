# Active Audio Chain Triage

Date: 2026-09-20
Scope: issues #73 through #79 in `edoworks/sf0.8`.

## Duplicate Review

The chain was reviewed against the live issue inventory and issue #80. #80 is
adjacent infrastructure for planner/writer handoff integrity, not a duplicate
of the audio product capability. Within the chain, #73 is the map; #74 is the
contract; #75 is the portable core/replay; #76 is bounded Mac live listening;
#77 is the Apple vertical slice; #78 is physical-device validation; and #79 is
real-cat/family acceptance. No duplicate was found.

## Classification And Priority

| Issue | Classification | Intended priority | Reason |
|---|---|---:|---|
| #73 | enhancement | P1 | End-to-end map for the selected capability |
| #74 | enhancement | P1 | Contract gate; completed |
| #75 | enhancement | P1 | Active portable-core dependency |
| #76 | enhancement | P2 | Host live-listening probe after core |
| #77 | enhancement | P1 | Product vertical slice required for customer-zero proof |
| #78 | enhancement | P2 | Physical-device gate after product slice |
| #79 | enhancement | P2 | Empirical family and real-cat acceptance |

## Reprioritization Review

No issue is promoted above #75 until the portable production boundary and
approved comparison fixtures are complete. #77 may proceed in parallel only if
it consumes the same core contract. Product A remains shelved and is not a
competing lane. #74 is complete and should not be reopened.

## Mutation Status

The global issue-intent guard now requires labels, matching classification,
P0-P3 priority, duplicate review, and reprioritization review for all new
issues. The active chain predates that guard and currently has empty remote
label sets. Historical/active backfill requires a separate owner-authorized
GitHub label mutation; this session did not claim that labels were applied.
