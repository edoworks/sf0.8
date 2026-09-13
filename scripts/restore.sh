#!/usr/bin/env bash
# restore.sh — restore an encrypted backup into a given directory.
#
# Quarterly drill step 6: restores the snapshot, then verify that Git still
# reconstructs intent (deleting factory.sqlite changes no product state).
set -euo pipefail

ARCHIVE="$1"                  # path to <stamp>.tar.enc
DEST="${2:-.}"                # restore into repo root
[ -z "${FACTORY_BACKUP_PASSPHRASE:-}" ] && { echo "FACTORY_BACKUP_PASSPHRASE not set" >&2; exit 1; }

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

openssl enc -d -aes-256-cbc -pbkdf2 -pass env:FACTORY_BACKUP_PASSPHRASE -in "$ARCHIVE" -out "$TMP/bundle.tar"
mkdir -p "$TMP/x"
tar -C "$TMP/x" -xf "$TMP/bundle.tar"
cp -R "$TMP/x/." "$DEST/"
echo "restored into $DEST"
