# Savehumanity Evidence Slice

Status: `LOCAL_EXPERIMENT_ONLY`
Cutoff: `2026-09-19`

## Scope

Decision: determine whether a provenance-first contribution workflow shows
material differentiation from ordinary ChatGPT plus current web search and
existing AI-safety directories. No product, catalog, refresh service, outreach,
submission, publication, or external write is authorized by this artifact.

Stopping rule: abstain if one currently wanted technical pathway cannot be
verified, if the baseline performs the same checks, or if causal claims cannot
be stated without false confidence.

## Workflow

`user constraints -> local evidence record -> status/want verification -> skill/time match -> card or abstention`

Run:

```bash
python3 scripts/contribution_card.py docs/research/savehumanity-opportunity.json --skills Python testing --hours 2
python3 -m unittest tests.test_contribution_card
```

The generator is local and deterministic. It does not retrieve URLs or treat
retrieved text as instructions. `source_verified` is a human-entered research
fact, not something the script asserts.

## Validation correction

Validation found that `expiry_date` was read as a hard gate but was absent from
the required evidence-field list. Malformed records therefore raised a
`KeyError` instead of producing the required explicit abstention.

Root-cause chain: the expiry gate was added as a runtime check; the schema list
was maintained separately; no test removed the expiry field; malformed input
reached direct indexing; the workflow violated its abstention contract. The
immediate correction adds `expiry_date` to the required fields. The recurrence
guard is a regression test asserting that a missing expiry produces `ABSTAIN`.

## Same-candidate baseline experiment

Retrieved and rechecked from canonical sources on `2026-09-19`:

- Issue #5369 API: open, labels `accepted` and `good first issue`, no assignee.
- PR #5410 API: open draft, body says `Closes #5369`, and implements the same
  proposed lowercase-`z` normalization.
- `CONTRIBUTING.md`: non-qualified contributors must start from an accepted
  issue, claim it, and check for existing open PRs; duplicates are closed in
  favor of the earlier PR.

| Criterion | Ordinary web research | Card before guard | Card after guard |
|---|---|---|---|
| Current issue status | Found open/accepted issue | Preserved | Preserved |
| Existing competing work | Found open draft PR #5410 | Not represented; emitted `CARD` | Required evidence; emits `ABSTAIN` |
| Contribution wanted now | Issue accepted, but duplicate work exists | Overstated | Correctly withheld |
| Source traceability | API and policy URLs available | One issue URL only | Issue, PR, and policy evidence retained |
| First step | Check PR/issue state before coding | Could encourage coding | Reverify after PR terminal state |

This is a concrete safety and usefulness improvement over the earlier slice,
but it is one manually performed case, not evidence for a standalone product.
The baseline still has no measured speed or real user-outcome advantage.

Root-cause chain for the competing-work defect: the evidence schema modeled
issue acceptance but not duplicate work; the generator checked acceptance only;
an open implementation of the same fix therefore still looked actionable; a
user could create review burden or duplicate a pending contribution; the
workflow's “wanted now” claim was too strong. The immediate correction adds a
competing-work field and abstention gate. The recurrence guard is the focused
regression test for an open competing PR.

## Candidate

One pathway was verified: Inspect AI issue #5369. The project source says its
non-qualified contributors must start from a maintainer-accepted issue; the
issue was open, accepted, marked good first issue, reproducible, bounded, and
unassigned at retrieval. This verifies a pathway, not a guarantee that a patch
will be accepted or materially reduce catastrophic risk.

## Baseline comparison

| Criterion | Ordinary ChatGPT + web search | This slice | Result |
|---|---|---|---|
| Current opportunity verification | Can perform it with explicit prompting | Requires a local evidence record and expiry | Observable discipline advantage; no speed evidence |
| Source correctness | Depends on prompt and browsing | Requires a supporting passage and direct verification flag | Observable schema advantage; not proof of correctness |
| Fact/inference distinction | Possible, not enforced | Separate fields and no impact score | Observable output difference |
| Stale/closed detection | Possible with careful browsing | Deterministic abstention | Observable guard |
| Wanted contribution | May confuse project existence with acceptance | Requires direct wanted evidence | Observable guard |
| Counterfactual and burden | Often omitted | Required card fields | Better visibility, causal value unknown |
| Actionability | Can suggest a next step | Produces one reversible step | Similar capability; no material superiority shown |

Existing directories are useful discovery sources. AISafety.com listed volunteer
projects and statuses, while AISafety.info offered general ways to help; neither
alone established that a specific technical task was currently wanted or
accepted. The Inspect issue and contribution policy supplied stronger primary
verification.

## Platform verification

Retrieved 2026-09-19 from official OpenAI documentation:

- `https://developers.openai.com/plugins`: Plugins may combine skills, MCP
  servers, and optional UI; the page links to the current documentation set.
- `https://developers.openai.com/plugins/concepts/skills`: Skills are folders
  with metadata and instructions for repeatable workflows; skills can work
  without an MCP server when no live data or controlled action is required.
- `https://developers.openai.com/plugins/app-guidelines`: published plugins
  must provide clear purpose, reliable behavior, accurate tool descriptions,
  minimal inputs, and correct `readOnlyHint`, `openWorldHint`, and
  `destructiveHint` annotations for MCP tools.
- `https://developers.openai.com/plugins/deploy/submission`: submission
  requires portal access, a verified developer/business identity, listing
  materials, and five positive plus three negative test cases. Remote MCP
  submissions require a stable public HTTPS endpoint.
- `https://help.openai.com/en/articles/10291617-scheduled-tasks-in-chatgpt`:
  scheduled tasks are account/app dependent, have plan-dependent active-task
  limits, and cannot access files uploaded to a project; event-triggered tasks
  require connected apps and authorization.
- `https://openai.com/policies/usage-policies/`: unsolicited safety testing,
  malicious system compromise, political campaigning/lobbying, and privacy
  violations are prohibited uses.

These sources establish platform requirements, not that a local capability is a
ChatGPT integration. No integration was built or tested. Open questions include
current account eligibility, review outcomes, and whether a skills-only package
would be accepted for this workflow.

## Critique

| Assumption | Evidence | Weakness | Consequence | Test/change |
|---|---|---|---|---|
| A separate product is needed | Direct verification required a project issue and policy | ChatGPT can perform the same steps | Product need is unproven | Compare time/error across repeated identical cases |
| Directories leave an opportunity-verification gap | Directory entries describe projects/statuses | Directory data may be current and useful | Gap may be narrow | Audit ten entries against project sources before building a catalog |
| We can distinguish wanted work | Accepted label plus issue-first policy | Labels can change; no maintainer conversation occurred | Reverification is mandatory | Recheck immediately before any user action |
| Matching constraints adds value | Explicit skills/time match | No user outcome observed | Actionability is only hypothesized | Observe whether a user takes the reversible step |
| Provenance improves decisions | Passage/date/status fields | Provenance can decorate weak causal claims | False confidence remains a central risk | Keep causal claims as inference/unknown and test rejection cases |
| Suggested work is net-positive | Small proposed fix | Review/duplicate burden remains | Do not encourage unsolicited coding | Require accepted issue and first reversible step |
| “Savehumanity” creates useful urgency | None | Framing may pressure users or imply impact | Use codename only; no duty/urgency language |

## Epistemic record

- `OBSERVED`: public issue state, labels, reproduction, proposed fix, project contribution rules.
- `ORGANIZATION CLAIM`: Inspect AI's stated contribution process and test commands.
- `EXPERT JUDGMENT`: effort estimate of two hours, based on issue scope; not a maintainer estimate.
- `FORECAST`: none made about acceptance or safety outcomes.
- `SCENARIO`: the patch is used in an evaluation workflow that handles lowercase-z timestamps.
- `OUR INFERENCE`: fixing the parser could remove an avoidable infrastructure failure.
- `UNKNOWN`: downstream use, safety relevance, acceptance, counterfactual value, and global impact.

## Adversarial results

The local tests cover fabricated/unverified citation, existing-but-unsupported

## Decision implications

- `BUILD`: supported only for this small local slice; not supported for a public product, catalog, scheduler, or integration.
- `SIMPLIFY`: supported because the verified value is mostly a disciplined prompt/schema and abstention rule.
- `CONTRIBUTE UPSTREAM`: plausible for the candidate, but blocked here by no external contribution authorization and by the project's required claim/PR route.
- `STOP`: supported if the baseline comparison shows no meaningful reduction in verification error or if maintenance cannot keep opportunity status current.

The smallest completed experiment was a human-controlled, same-candidate
comparison of ordinary web research and this local card. It found a material
duplicate-work guard, but does not justify a public product. The next decision
experiment should use a second independent opportunity only if authorized; do
not run it automatically or contact project owners.
