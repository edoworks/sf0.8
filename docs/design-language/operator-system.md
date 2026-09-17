# Operator System

The operator system serves factory surfaces where trust, status, and evidence
matter more than brand expression.

## Reference surfaces

The first reference slice should cover:

1. Queue or work board.
2. Run or increment detail.
3. Verification and evidence view.
4. Blocked, failed, or ambiguous state.
5. Approval and handoff.
6. Recovery or audit history.

## Information hierarchy

Every surface should answer, in order:

1. What is this item?
2. What is its current state?
3. What evidence supports that state?
4. What action is safe and available next?
5. What changes if the operator takes that action?

## State vocabulary

Use explicit labels and semantic styling for:

- Proposed
- In progress
- Awaiting human input
- Verified
- Blocked
- Failed
- Superseded
- Rejected
- Unknown or stale

Do not represent these states with color alone. State changes should include a
timestamp, actor or source, and relevant evidence when available.

## Interaction rules

- Destructive or external-impact actions require an explicit confirmation and
  a clear description of impact.
- Reversible actions should make reversal visible.
- Evidence should be reachable from the state it supports.
- Long-running work should expose progress and last-known update time.
- Errors should distinguish operator action, retryable infrastructure failure,
  and product defect.
- Empty states should explain whether there is no work, no permission, or no
  data yet.

## Visual direction

- Neutral surfaces with restrained semantic accents.
- Red is reserved for material danger or failure, not ordinary attention.
- Use compact summaries for scanning and expandable detail for investigation.
- Prefer tables, timelines, and structured evidence to decorative cards.
- Use density deliberately: enough information for a decision, never enough to
  hide the decision.

## iPad and desktop behavior

- Persistent navigation should remain available when space permits.
- A selected item should open beside the queue rather than replacing it when a
  two-column layout improves comparison.
- Keyboard navigation and pointer hover states are required for operator tools.
- Touch targets remain usable on iPad even when the interface is dense.
