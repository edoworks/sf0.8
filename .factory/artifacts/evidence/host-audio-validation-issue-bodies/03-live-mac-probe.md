# Parent

#73

# Blocked by

Portable production audio core and explicit owner enrollment.

# Outcome

Add a visible, bounded, owner-started Mac microphone probe that exercises the
same production core without becoming unattended household surveillance.

# Acceptance criteria

- Every listening session requires an explicit start and has a bounded end.
- Microphone use is visible and macOS consent remains OS-mediated.
- Permission denial fails closed; no login item, daemon, or TCC workaround is
  introduced.
- Raw rolling audio is transient by default and network access is absent.
- A locally retained event can be replayed and deleted by the owner.
- Evidence records metadata and outcomes, not household audio.

# Verification

- Swift unit and integration tests
- Signed/local host permission and denial checks
- Owner-started live probe observation
