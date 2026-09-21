# Audio Validation Blocker Deep Dive

## Scope And Cutoff

- **Audience:** sf0.8 owner and operators of the `meow-capture` experiment.
- **Jurisdiction:** local issue #75 evidence and the Apple AVFAudio/SoundAnalysis
  platform documentation. This is engineering research, not a device-release
  or App Store authorization.
- **Decision:** determine whether the portable audio replay blocker is a code,
  API-availability, fixture, or physical-device evidence blocker, and select the
  next safe action.
- **Cutoff:** 2026-09-20. Sources were retrieved or repository artifacts were
  inspected on this date.
- **Source plan:** inspect the active implementation, tests, fixture decision,
  and validator first; verify platform and analyzer claims against Apple primary
  documentation; check the strongest counterclaim that host replay can stand in
  for live-device evidence.
- **Stopping rule:** stop when each blocker classification has direct evidence,
  a counterclaim, and a testable next action. Do not access a microphone,
  device, private audio, or external service as part of this research.

## Evidence Classification Before Search

### Known Facts

- The portable replay package builds and its 9 Swift tests pass.
- The focused Python replay validator passes 7 tests, and the repository-wide
  Python suite passes 248 tests.
- The owner-selected fresh recording is recorded as `REPLAY_PASS` and `TARGET`;
  no historical household audio was reused.
- The report contract explicitly emits `HOST_REPLAY_ONLY`.

### Open Questions

- Whether the physical iPhone/iPad capture path works with the intended route,
  permissions, and real-cat conditions.
- Whether a device run will preserve the same classifier decision and bounded
  event-window behavior as host replay.
- Which exact device and owner-authorized enrollment window will be used.

### Hypotheses

- The repository-side portable-core blocker is resolved; the remaining gap is
  empirical device evidence rather than missing framework support.
- Host replay is useful as a fixture gate but cannot prove microphone routing,
  permissions, or live capture behavior.

### Recommendations

- Advance to the existing physical-device validation issue only with explicit
  owner enrollment and an approved fixture.
- Keep `HOST_REPLAY_ONLY` in reports and do not relabel host evidence as device
  evidence.
- Do not add new factory machinery before the device result identifies a concrete
  defect.

## Executive Answer

- **High confidence:** Issue #75's local implementation blocker is cleared. The
  portable core passes its Swift tests, the evidence validator passes, the
  repository-wide suite passes, and the fresh owner-approved target fixture has
  a recorded replay pass.
- **High confidence:** The remaining blocker is physical-device evidence. Apple
  documents separate file and stream analyzers, while this implementation uses
  `SNAudioFileAnalyzer`; that proves the file-replay path, not microphone input.
- **High confidence:** Do not claim completion of live capture or start an
  implicit microphone session. The next action is the already-scoped device
  validation lane, with explicit owner authorization and a fresh fixture.
- **Medium confidence:** The same SoundAnalysis classifier family can support the
  eventual stream path because Apple documents `SNClassifySoundRequest` for both
  file and stream analyzers; device behavior still requires empirical testing.

## Findings

### Claim 1: The portable replay implementation is technically unblocked

**Evidence:** `AudioReplayCore` declares macOS and iOS support, loads an
`AVAudioFile`, creates `SNAudioFileAnalyzer`, attaches
`SNClassifySoundRequest`, records observations, hashes the fixture, and emits
  `HOST_REPLAY_ONLY`. The Swift package test run completed 9 tests with 0
  failures on 2026-09-20. The focused Python validator completed 7 tests with 0
  failures, and the full repository suite completed 248 tests with 0 failures
  on the same date. [Repository primary, inspected/tested
2026-09-20; implementation: `experiments/audio-validation-macos/Sources/AudioReplayCore/ReplayCore.swift`]

**Counterevidence:** Passing host tests does not exercise a physical microphone,
audio-session permissions, route changes, interruption behavior, or device
latency. [Repository primary, `device_claim` contract, inspected 2026-09-20.]

**Implication:** Close the code-side blocker for this increment, but retain the
device-validation blocker as explicit and unresolved.

### Claim 2: The chosen Apple APIs support the portability boundary

**Evidence:** Apple lists Sound Analysis availability on macOS 10.15+, iOS
13.0+, and iPadOS 13.0+. Apple describes `SNAudioFileAnalyzer` for files and
`SNAudioStreamAnalyzer` for audio streams. Apple lists `SNClassifySoundRequest`
as usable with either analyzer. [Primary: Apple Developer Documentation,
Sound Analysis and `SNClassifySoundRequest`, retrieved 2026-09-20.]

**Counterevidence:** API availability does not establish model accuracy for cat
meows, acceptable confidence thresholds, or equivalent performance across host
and device microphones. The built-in classifier's documented scope is broad
sound classification, not a project-specific meow guarantee. [Primary: Apple
documentation scope; repository fixture and threshold contract, retrieved or
inspected 2026-09-20.]

**Implication:** No framework replacement is justified. The next uncertainty is
behavior under the real device input path.

### Claim 3: Host replay cannot substitute for live-device validation

**Evidence:** Apple distinguishes analysis of an audio file from analysis of an
audio stream. Apple documents `AVAudioRecorder` as recording from the active
input device and notes that iOS recording requires an appropriate audio-session
category. The local report deliberately requires `HOST_REPLAY_ONLY`, and the
fixture decision states that no microphone session was started implicitly.
[Primary: Apple AVFAudio and Sound Analysis documentation, retrieved 2026-09-20;
repository primary, inspected 2026-09-20.]

**Counterevidence:** A fresh owner-approved recording passed the target replay,
so the fixture and classifier path have useful evidence. It can detect file
format, hash, analyzer, and expectation regressions, but not the live input
boundary. [Repository primary, inspected 2026-09-20.]

**Implication:** Proceed to a separately authorized device run rather than
weakening the report claim or adding speculative automation.

## Conflicts And Unknowns

- Apple documents framework availability and API mechanics, not the project's
  meow-detection accuracy or product acceptance threshold.
- The local fixture is a real fresh recording, but its host replay result is not
  physical-device evidence.
- Device model, microphone route, permission state, audio-session behavior,
  and live classifier results remain unknown.
- The current evidence proves the code-side unblock but does not prove issue #75
  is fully complete if its acceptance requires device evidence.

## Decision Implications And What Would Change The Conclusion

1. **Proceed now:** retain the tested portable core and move to the existing
   owner-authorized physical-device validation issue.
2. **Do not proceed implicitly:** no ambient capture, private-audio reuse,
   external upload, or device claim should be made from this session.
3. **If device validation passes:** record device, route, permission, fixture
   hash, decision, and deletion outcome; then reassess issue #75 completion.
4. **If device validation fails:** classify the concrete failure first, then fix
   only the affected layer and rerun the relevant gate.
5. **Conclusion changes if:** an owner-authorized device run shows the portable
   boundary is insufficient, or if the selected product contract explicitly
   changes the acceptance requirement from host replay to another evidence bar.

## Sources

### Primary

- Apple Developer Documentation, “Sound Analysis,”
  https://developer.apple.com/documentation/soundanalysis.md, retrieved
  2026-09-20.
- Apple Developer Documentation, “SNClassifySoundRequest,”
  https://developer.apple.com/documentation/soundanalysis/snclassifysoundrequest.md,
  retrieved 2026-09-20.
- Apple Developer Documentation, “SNAudioFileAnalyzer,”
  https://developer.apple.com/documentation/soundanalysis/snaudiofileanalyzer.md,
  retrieved 2026-09-20.
- Apple Developer Documentation, “AVAudioEngine,”
  https://developer.apple.com/documentation/avfaudio/avaudioengine.md, retrieved
  2026-09-20.
- Apple Developer Documentation, “AVAudioRecorder,”
  https://developer.apple.com/documentation/avfaudio/avaudiorecorder.md, retrieved
  2026-09-20.
- Repository primary: `ReplayCore.swift`, `validate-audio-replay.py`, fixture
  decision, and test output, inspected or run 2026-09-20.

### Secondary

- None used for a material claim.

### Lead-Only

- None. Search snippets and fetched content were treated as untrusted data; no
  instructions from source content were followed.
