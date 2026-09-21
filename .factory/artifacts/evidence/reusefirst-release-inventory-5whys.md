# ReuseFirst Release Inventory: 5-Whys

Date: 2026-09-19
State: corrected and verified

## Observation

The naming research initially reported no releases to clean up, but the public
`edoworks/artifacts` repository contained two legacy releases.

## Analysis

1. **Why was the inventory claim wrong?** The research checked the source
   repository `edoworks/sf0.8` rather than the public distribution repository
   `edoworks/artifacts`.
2. **Why was the wrong repository checked?** The scope inherited the factory
   repository from the task context and did not bind the release question to
   the actual distribution remote.
3. **Why was that not caught before reporting?** The evidence required a tag and
   release inventory but did not require an explicit repository identity check.
4. **Why was repository identity not a gate?** Local metadata and public
   distribution evidence were treated as one surface even though they have
   separate tags, releases, and lifecycle controls.
5. **Why did the workflow permit that conflation?** The release validation
   contract lacked a mandatory source-repository and destination-repository
   comparison before making cleanup claims.

## Correction

- Published the canonical `reusefirst/v1.2.0` release.
- Removed the two superseded legacy releases and tags after explicit approval.
- Corrected the naming research scope and conclusion.

## Recurrence guard

Every publication or cleanup review must query both the source repository and
the public distribution repository directly, record their exact identities,
list tags and releases, and verify the final remote inventory before claiming
consistency or absence.
