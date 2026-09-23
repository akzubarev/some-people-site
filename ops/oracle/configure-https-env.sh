#!/usr/bin/env bash
set -Eeuo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
env_file="${ENV_FILE:-$repo_root/backend/.env}"
mode="${1:-}"

[[ "$mode" == "prepare" || "$mode" == "activate" ]] || {
  echo "Usage: $0 <prepare|activate>" >&2
  exit 2
}
[[ -f "$env_file" ]] || { echo "Missing $env_file" >&2; exit 1; }

set_env() {
  local key="$1"
  local value="$2"
  local temporary
  temporary="$(mktemp "${env_file}.tmp.XXXXXX")"
  awk -v key="$key" -v value="$value" '
    BEGIN { found = 0 }
    index($0, key "=") == 1 { print key "=" value; found = 1; next }
    { print }
    END { if (!found) print key "=" value }
  ' "$env_file" > "$temporary"
  install -m 0600 "$temporary" "$env_file"
  rm -f "$temporary"
}

set_env CSRF_COOKIE_SECURE 1
set_env SESSION_COOKIE_SECURE 1
set_env TRUST_X_FORWARDED_PROTO 1
set_env SECURE_SSL_REDIRECT "$([[ "$mode" == "activate" ]] && echo 1 || echo 0)"
set_env SECURE_HSTS_SECONDS 0
set_env SECURE_HSTS_INCLUDE_SUBDOMAINS 0
set_env SECURE_HSTS_PRELOAD 0

echo "HTTPS environment flags configured in $mode mode"
