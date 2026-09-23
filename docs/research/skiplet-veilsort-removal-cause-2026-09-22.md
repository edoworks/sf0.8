# Skiplet and Veilsort Removal-Cause Learning

Date: 2026-09-22
Owner: hellofoculoom
Subject: why Skiplet and Veilsort were removed from the App Store
Status: cause recorded by owner; recurrence guard already in place

## Cause (owner-stated, 2026-09-22)

Skiplet and Veilsort were removed from the App Store because:

1. They were not factory-created — they predated the factory paved road and
   lacked deterministic verification, evidence generation, and recovery
   contracts.
2. They were hard to maintain and fix bugs — without the factory's verify
   loop, reproducing and fixing issues required disproportionate manual
   effort.
3. They did not meet the owner's quality bar — the gap between the shipped
   state and the owner's standard was large enough that removing them was
   preferable to maintaining them.

This is a **quality and maintainability decision**, not an Apple takedown or
policy violation. The owner chose to remove them.

## 5-Whys

1. Why were Skiplet and Veilsort removed? They did not meet the owner's
   quality bar and were hard to maintain.
2. Why were they hard to maintain? They were not factory-created; they lacked
   deterministic verification, evidence generation, and recovery contracts.
3. Why were they not factory-created? They predated the factory; the factory
   was built partly because of the pain of maintaining them without it.
4. Why did they not meet the quality bar? Without the factory's verify loop,
   bugs were harder to catch and fix, and the shipped state drifted from the
   owner's standard.
5. Root cause: **shipping apps without a factory paved road creates
   maintainability debt that eventually exceeds the value of keeping the app
   in the store.**

## Recurrence Guard

The recurrence guard is already in place:

- The factory PRD requires all reference apps to be created from a downloaded
  factory release, verified deterministically, and qualified through the
  release ladder (G1-G11) before Apple submission.
- The portfolio-focus admission rule requires owner-approved issues for any
  new product or surface.
- The factory's Recovery Law (PRD line 53-56) requires every failure to have
  a machine-readable classification and a documented recovery path.
- The qualification ledger (issue #11) requires 30-day unattended success
  before v0.2.0 promotion.

No new guard is needed. The existing factory contracts are the direct response
to this learning. The learning confirms that the factory's existence is
itself the recurrence guard.

## Implication for NowNest

NowNest is factory-created, has 33 unit tests + 30 UI tests on each simulator
family, static analysis is clean, G8 and G9 passed, and the archive is built.
It is being qualified through the release ladder precisely to avoid the
Skiplet/Veilsort maintainability trap.

## Evidence

- `apple-history.json`: Skiplet → `REMOVED_FROM_APP_STORE`, Veilsort →
  `REMOVED_FROM_APP_STORE`
- `portfolio.yaml`: both marked `lifecycle: dormant`
- Owner statement: 2026-09-22 (this session)
- No Apple takedown or policy violation was involved