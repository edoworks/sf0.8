#!/usr/bin/env bash
# backup.sh — encrypted off-device backup for the disposable-private control state.
#
# Backs up: factory.sqlite + private manifests. Encrypted; restore path is
# restore.sh. RPO ≤24h per metrics doc. Key lives in your secret manager —
# this script never stores it.
set -euo pipefail

DB="${FACTORY_DB:-.factory/factory.sqlite}"
BACKUP_DIR="${FACTORY_BACKUP_DIR:-$HOME/factory-backups}"
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
OUT="$BACKUP_DIR/$STAMP"

mkdir -p "$OUT"
[ -f "$DB" ] && cp "$DB" "$OUT/factory.sqlite"
[ -f .factory/governance.yaml ] && cp .factory/governance.yaml "$OUT/"

# Encrypt with a passphrase from the environment (never hardcoded).
# FACTORY_BACKUP_PASSPHRASE read from secret manager by the caller.
if [ -z "${FACTORY_BACKUP_PASSPHRASE:-}" ]; then
  echo "FACTORY_BACKUP_PASSPHRASE not set — refusing unencrypted backup" >&2
  exit 1
fi

tar -C "$OUT" -cf - . | openssl enc -aes-256-cbc -pbkdf2 -pass env:FACTORY_BACKUP_PASSPHRASE -out "$BACKUP_DIR/$STAMP.tar.enc"
rm -rf "$OUT"
echo "backup: $BACKUP_DIR/$STAMP.tar.enc"
