# Scope

Add a governed reach-signal contract for reusable primitives. Record downloads as reach only. Permit external usage evidence only when a non-founder provides consented, revision-linked execution/workflow evidence. Do not add telemetry, identify users covertly, publish artifacts, or change release authority.

## Acceptance criteria

- Raw downloads cannot advance usage, retention, economic, or payment evidence.
- Verified external use requires non-founder status, consent, immutable revision, execution evidence, workflow, and job-to-be-done.
- Founder, automated, anonymous, or unconsented signals cannot satisfy external-use evidence.
- Reach signals are stored separately from the five market-evidence levels.
- Duplicate and unknown primitive references are rejected.
- No publication, outreach, telemetry, IP inference, or external mutation occurs.

## Verification

```text
python3 scripts/validate-primitive-reach.py
python3 -m unittest tests.test_primitive_reach
python3 -m unittest discover -s tests -p 'test_*.py'
```

## Safety boundary

The factory may validate supplied evidence and prepare a recommendation. It may not identify downloaders, contact users, publish releases, or infer identity from network data.
