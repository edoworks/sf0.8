# Rung Public Origin Context — 2026-09-14

This is private operational context. It preserves the historical serving model
without publishing credentials, host paths, or Cloudflare resource identifiers.

## Confirmed history

- `sf0.1/docs/RELEASE_DISTRIBUTION.md` describes static website delivery through
  Cloudflare DNS and GitHub Pages.
- `sf0.5/docs/product/PRD-006.json` records that the public Rung surface was
  served from one operator laptop through Docker, a deployment router, and a
  Cloudflare Tunnel.
- `sf0.5/docs/exec-plans/completed/0024-distribution-plane-separation-proposal.json`
  records the public-availability risk when the tunnel and serving path shared
  the construction host and compose networks.
- `sf0.5/compose.public.yaml` was the corrective standalone connector design;
  its documented contract was edge-only networking, restart protection, and
  independence from factory compose teardown.
- `sf0.5/factory/evidence/index.json` records later live HTTP 200 probes for the
  Rung landing page and CLI download after that corrective work.
- The current public probe returns Cloudflare HTTP 530. The current origin is
  not identified by repository contents or public DNS alone.

## Cloudflare account inspection

- The `edoworks.com` zone is active on the Free Website plan.
- `rung.edoworks.com` is a proxied CNAME to a `cfargotunnel.com` hostname.
- The account currently has no non-deleted Cloudflare Tunnels.
- The available DNS-scoped credential can inspect the record but cannot edit
  Cloudflare Redirect Rules.
- Therefore the 530 is confirmed as a stale Tunnel route, and the safe fix is
  either a Cloudflare redirect rule to `/rung/` or a deliberately rebuilt,
  independently monitored Tunnel. A DNS-only CNAME change would not provide
  the required path redirect and was not made.

## 5-Whys

1. Why is `rung.edoworks.com` unavailable? The public probe returns HTTP 530.
2. Why does the edge return 530? Cloudflare cannot obtain or serve a valid
   response from the configured origin.
3. Why is the origin uncertain? The historical origin was a laptop-hosted
   Docker/Tunnel serving chain, while the current Rung repository contains only
   artifact release paths and no web deployment workflow.
4. Why can the historical chain no longer be assumed? sf0.5 is deprecated and
   its operational host state is not the authority for current Rung delivery.
5. Why was the stale public URL not caught earlier? Public metadata and website
   links lacked an independent external health check and a current hosting
   source-of-truth record.

## Correction

- Artifact correction: Rung release artifacts are explicitly validated without
  Docker or a container runtime.
- Distribution correction: restore the domain only after the owner identifies
  the origin, or replace the laptop-hosted web path with a verified static or
  managed host.
- Recurrence guard: maintain an external URL smoke check independent of build
  CI, and keep public metadata synchronized with the verified destination.

The exact Cloudflare sub-cause remains an owner-only investigation item.
