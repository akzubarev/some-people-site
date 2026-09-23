#!/usr/bin/env bash
set -Eeuo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
compose_file="$repo_root/docker/docker-compose.prod.yaml"
env_file="$repo_root/backend/.env"
restore_dump=""

usage() {
  cat <<'EOF'
Usage: ./ops/oracle/deploy.sh [--restore /absolute/path/to/database.dump]

Build and start the OCI web/API stack on 127.0.0.1:8080. The Telegram bot is
left unchanged. --restore is accepted only while the target database has no
user tables and the bot is stopped.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --restore)
      [[ $# -ge 2 ]] || { echo "--restore requires a dump path" >&2; exit 2; }
      restore_dump="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

command -v docker >/dev/null 2>&1 || { echo "Docker is required" >&2; exit 127; }
command -v curl >/dev/null 2>&1 || { echo "curl is required" >&2; exit 127; }
command -v setfacl >/dev/null 2>&1 || { echo "Install the acl package for nginx static access" >&2; exit 127; }
[[ -f "$env_file" ]] || { echo "Missing $env_file" >&2; exit 1; }
[[ -z "$restore_dump" || -f "$restore_dump" ]] || { echo "Dump not found: $restore_dump" >&2; exit 1; }

install -d -m 0750 \
  "$repo_root/runtime/logs" \
  "$repo_root/runtime/media" \
  "$repo_root/runtime/staticfiles"

compose=(docker compose -f "$compose_file")

"${compose[@]}" config --quiet
"${compose[@]}" build api web
"${compose[@]}" up --detach postgresql

database_container="$("${compose[@]}" ps --quiet postgresql)"
for _ in {1..60}; do
  if [[ "$(docker inspect --format '{{.State.Health.Status}}' "$database_container")" == "healthy" ]]; then
    break
  fi
  sleep 2
done

[[ "$(docker inspect --format '{{.State.Health.Status}}' "$database_container")" == "healthy" ]] || {
  echo "PostgreSQL did not become healthy" >&2
  exit 1
}

if [[ -n "$restore_dump" ]]; then
  if "${compose[@]}" --profile bot ps --status running --services | grep -qx bot; then
    echo "Refusing to restore while the bot is running" >&2
    exit 1
  fi
  db_user="$("${compose[@]}" exec -T postgresql printenv POSTGRES_USER)"
  db_name="$("${compose[@]}" exec -T postgresql printenv POSTGRES_DB)"
  table_count="$("${compose[@]}" exec -T postgresql psql \
    --username "$db_user" \
    --dbname "$db_name" \
    --tuples-only \
    --no-align \
    --command "SELECT count(*) FROM pg_catalog.pg_tables WHERE schemaname NOT IN ('pg_catalog', 'information_schema');")"

  [[ "$table_count" == "0" ]] || {
    echo "Refusing to restore into a database that already has user tables" >&2
    exit 1
  }

  "${compose[@]}" exec -T postgresql pg_restore --list < "$restore_dump" >/dev/null
  "${compose[@]}" exec -T postgresql pg_restore \
    --exit-on-error \
    --no-owner \
    --no-privileges \
    --username "$db_user" \
    --dbname "$db_name" < "$restore_dump"
fi

"${compose[@]}" run --rm api python manage.py migrate --noinput
"${compose[@]}" run --rm api python manage.py collectstatic --noinput
"${compose[@]}" run --rm api python manage.py check
"${compose[@]}" up --detach api web

# The nginx worker has a different UID from Django. Grant only that UID access
# to the static root; other local accounts retain the original restrictions.
nginx_uid="$("${compose[@]}" exec -T web id -u nginx)"
[[ "$nginx_uid" =~ ^[0-9]+$ ]] || { echo "Invalid nginx UID" >&2; exit 1; }
setfacl -m "u:${nginx_uid}:rx" "$repo_root/runtime/staticfiles"

for _ in {1..60}; do
  if curl --fail --silent http://127.0.0.1:8080/healthz >/dev/null; then
    break
  fi
  sleep 2
done

curl --fail --silent --show-error http://127.0.0.1:8080/healthz >/dev/null
curl --fail --silent --show-error http://127.0.0.1:8080/ >/dev/null
curl --fail --silent --show-error http://127.0.0.1:8080/staticfiles/jazzmin/css/main.css >/dev/null

"${compose[@]}" ps
