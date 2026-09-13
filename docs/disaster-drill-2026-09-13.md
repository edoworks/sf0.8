# Disaster-recovery drill — 2026-09-13

**Scenario:** blank machine; lost device; only forge credentials + backup passphrase survive.

## Pass conditions (all met)

1. Clone `edoworks/product-a` and `edoworks/sf0.8` from origin (not local disk) via gh credential helper. ✅
2. `./scripts/doctor.sh` green on clean checkout (Xcode 26.6 present; environment reproducible). ✅
3. `./scripts/verify.sh` **TEST SUCCEEDED** from a clean product-a clone (48 cases, iPhone 17 Pro). ✅
4. Encrypted backup `~/factory-backups/20260913T170220Z.tar.enc` restored into the sf0.8 clone via `scripts/restore.sh`; SQLite intact (1 run recorded). ✅
5. **Disposability invariant:** with `factory.sqlite` deleted, NORTH_STAR.md, docs/factory-v0.1-design-review.md, .factory/governance.yaml, roadmap — all still present in Git. Product intent reconstructable without the DB. ✅
6. Drill directory removed after pass.

## Observed RPO/RTO

- RPO: ≤1 second (backup at 17:02 UTC same session, no data between).
- RTO: ≈6 minutes (clone×2 + doctor + verify) on a warm machine. Cold-machine provisioning adds Xcode install.

## Findings to fix before next drill

- **SSH keys not configured** for this machine's github account — recovery currently depends on `gh auth`. For a true blank-machine recovery we must either configure ssh keys or ensure gh auth works from cold state. Recorded; owner decides.
- Backup location is local (`~/factory-backups`). True off-device copy is still an owner action (external drive / cloud vault) before RPO ≤24h claim holds against hardware loss.

## Next drill

Quarterly per roadmap; next due before 2026-12-13.
