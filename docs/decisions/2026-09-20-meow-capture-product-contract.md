# Meow Capture Product Contract

Date: 2026-09-20
Parent: [Host-side audio validation E2E](https://github.com/edoworks/sf0.8/issues/73)
Active increment: [Define new meow-capture app contract](https://github.com/edoworks/sf0.8/issues/74)

## Decision

Create a new, narrow iOS/iPadOS meow-capture experiment as the first consumer
of the host audio-validation capability. `meow-capture` is an internal working
identifier, not an authorized public name. Product A remains shelved and is not
revived by this decision.

## Owner-Visible Acceptance Sentence

During a bounded, owner-supervised session on a physical Apple device, the app
automatically retains a likely cat meow and lets the owner audibly replay and
delete that exact local clip without developer tooling.

## Minimum Session

1. The owner explicitly starts a bounded listening session.
2. The app visibly indicates microphone use and permission state.
3. The production pipeline identifies a likely cat vocalization and retains a
   bounded event clip with enough pre-roll and post-roll to be recognizable.
4. The owner can replay and delete the clip locally.
5. The session stops explicitly or at its declared time bound.

## Product Laws

- No fake classifier result may satisfy the acceptance sentence.
- Mac replay and Mac live listening are host evidence, never iPhone/iPad proof.
- Raw household audio stays local and is absent from Git, CI, logs, issue
  comments, and durable factory evidence.
- Microphone permission remains OS-mediated and denial fails closed.
- Listening is visible, owner-started, bounded, and never a daemon or login
  item.
- The first usable slice makes no translation, emotion, health, welfare, or
  veterinary claim.

## Initial Scope

- Shared normalized audio and event-classification boundary.
- Confidence threshold and explicit abstention.
- Bounded rolling buffer with event pre-roll and post-roll.
- Local replay and deletion.
- Deliberate first-launch, listening, captured-event, empty, permission-denied,
  and failure states on iPhone and iPad.

## Deferred

- Public identity, external repository, TestFlight, App Store submission,
  accounts, sync, cloud processing, analytics, sharing, interpretation,
  subscriptions, and generalized factory extraction.

## Stop Rules

Stop or re-scope if approved fixtures cannot distinguish target from common
non-target audio, automatic capture routinely misses recognizable meows,
false captures make the app burdensome, retained audio cannot be kept local,
or reliable operation requires unattended ambient surveillance.

## Evidence Classes

| Claim | Required evidence |
|---|---|
| Mapping, thresholds, buffering, deletion logic | Automated unit tests |
| Approved files pass through production core | Mac fixture replay |
| Bounded host microphone path works | Owner-started Mac probe |
| UI and deterministic lifecycle work | iOS Simulator tests and renders |
| Permissions, routes, microphone, playback, interruption recovery | Physical iPhone and iPad |
| A real meow is useful and the app is understandable | Owner-supervised real-cat and family observation |

## Authority

This contract authorizes local design and implementation under the existing
sf0.8 issue chain. It does not authorize ambient listening, publication,
external repository creation, TestFlight, App Store submission, spending, or
reuse of private household recordings as committed fixtures.

The first real-meow replay is separately owner-gated in the canonical human
action queue because historical audio provenance and consent cannot be inferred.
