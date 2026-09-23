#!/usr/bin/env bash
set -Eeuo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
env_file="$repo_root/backend/.env"
backup_dir="${BACKUP_DIR:-/srv/backups/some-people-site}"

[[ "${1:-}" == "--confirm-verified-copy" ]] || {
  echo "Usage: $0 --confirm-verified-copy" >&2
  exit 2
}
[[ -f "$env_file" ]] || { echo "Missing production environment" >&2; exit 1; }
storage_count="$(grep -c '^MEDIA_STORAGE=' "$env_file" || true)"
[[ "$storage_count" == "0" || "$storage_count" == "1" ]] || {
  echo "Expected at most one MEDIA_STORAGE setting" >&2
  exit 1
}
if [[ "$storage_count" == "1" ]]; then
  grep -q '^MEDIA_STORAGE=local$' "$env_file" || {
    echo "Expected MEDIA_STORAGE=local before activation" >&2
    exit 1
  }
fi

for key in MEDIA_S3_ENDPOINT_URL MEDIA_S3_REGION MEDIA_S3_BUCKET \
           MEDIA_S3_ACCESS_KEY_ID MEDIA_S3_SECRET_ACCESS_KEY; do
  grep -q "^${key}=." "$env_file" || {
    echo "Missing required media setting: $key" >&2
    exit 1
  }
done

install -d -m 0700 "$backup_dir"
backup="$backup_dir/backend.env.before-s3-$(date -u +%Y%m%dT%H%M%SZ).bak"
install -m 0600 "$env_file" "$backup"

temporary="$(mktemp "${env_file}.tmp.XXXXXX")"
trap 'rm -f "$temporary"' EXIT
awk -v append_setting="$([[ "$storage_count" == "0" ]] && echo 1 || echo 0)" '
  /^MEDIA_STORAGE=local$/ { print "MEDIA_STORAGE=s3"; next }
  { print }
  END { if (append_setting == 1) print "MEDIA_STORAGE=s3" }
' "$env_file" > "$temporary"
chmod 0600 "$temporary"
mv -- "$temporary" "$env_file"
trap - EXIT

echo "S3 media enabled; local media and previous environment retained"
