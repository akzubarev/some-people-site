#!/usr/bin/env bash
set -Eeuo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
backup_dir="${BACKUP_DIR:-/srv/backups/some-people-site}"
compose=(docker compose -f "$repo_root/docker/docker-compose.prod.yaml")

[[ -f "$repo_root/backend/.env" ]] || { echo "Missing production environment" >&2; exit 1; }
[[ "${1:-}" == "--upload" ]] || { echo "Usage: $0 --upload" >&2; exit 2; }
"${compose[@]}" config --quiet
"${compose[@]}" exec -T postgresql pg_isready >/dev/null

db_user="$("${compose[@]}" exec -T postgresql printenv POSTGRES_USER)"
db_name="$("${compose[@]}" exec -T postgresql printenv POSTGRES_DB)"
[[ "$db_user" =~ ^[A-Za-z_][A-Za-z0-9_]*$ ]] || { echo "Unsafe database user" >&2; exit 1; }
[[ "$db_name" =~ ^[A-Za-z_][A-Za-z0-9_]*$ ]] || { echo "Unsafe database name" >&2; exit 1; }

umask 077
install -d -m 0700 "$backup_dir"
timestamp="$(date -u +%Y%m%dT%H%M%SZ)"
filename="${db_name}-${timestamp}-$(od -An -N4 -tx1 /dev/urandom | tr -d ' \n').dump"
temporary="$(mktemp "$backup_dir/.database-XXXXXX")"
trap 'rm -f "$temporary"' EXIT

"${compose[@]}" exec -T postgresql pg_dump \
  --format=custom --no-owner --no-privileges \
  --username "$db_user" --dbname "$db_name" > "$temporary"
"${compose[@]}" exec -T postgresql pg_restore --list < "$temporary" >/dev/null
[[ -s "$temporary" ]] || { echo "Empty database dump" >&2; exit 1; }
mv -- "$temporary" "$backup_dir/$filename"
trap - EXIT

key="database-backups/${timestamp:0:4}/${timestamp:4:2}/$filename"
"${compose[@]}" run --rm --no-deps \
  -v "$backup_dir:/backup:ro" \
  -v "$repo_root/ops/oracle/upload-database-backup.py:/opt/upload-database-backup.py:ro" \
  api python /opt/upload-database-backup.py "/backup/$filename" "$key"

echo "Database backup retained locally and verified in Object Storage: $filename"
