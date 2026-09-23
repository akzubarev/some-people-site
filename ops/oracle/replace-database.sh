#!/usr/bin/env bash
set -Eeuo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
compose_file="$repo_root/docker/docker-compose.prod.yaml"
dump_path="${1:-}"
confirmation="${2:-}"
backup_dir="${BACKUP_DIR:-/srv/backups/some-people-site}"

usage() {
  echo "Usage: sudo $0 /absolute/path/to/database.dump --confirm-replace" >&2
}

[[ -n "$dump_path" && "$confirmation" == "--confirm-replace" ]] || { usage; exit 2; }
[[ "$dump_path" == /* ]] || { echo "Dump path must be absolute" >&2; exit 2; }
[[ -f "$dump_path" ]] || { echo "Dump not found: $dump_path" >&2; exit 1; }
[[ -f "$repo_root/backend/.env" ]] || { echo "Missing backend/.env" >&2; exit 1; }

compose=(docker compose -f "$compose_file")
"${compose[@]}" config --quiet
"${compose[@]}" up --detach postgresql

database_container="$("${compose[@]}" ps --quiet postgresql)"
for _ in {1..60}; do
  [[ "$(docker inspect --format '{{.State.Health.Status}}' "$database_container")" == "healthy" ]] && break
  sleep 2
done
[[ "$(docker inspect --format '{{.State.Health.Status}}' "$database_container")" == "healthy" ]] || {
  echo "PostgreSQL did not become healthy" >&2
  exit 1
}

db_user="$("${compose[@]}" exec -T postgresql printenv POSTGRES_USER)"
db_name="$("${compose[@]}" exec -T postgresql printenv POSTGRES_DB)"
[[ "$db_user" =~ ^[A-Za-z_][A-Za-z0-9_]*$ ]] || { echo "Unsafe database user name" >&2; exit 1; }
[[ "$db_name" =~ ^[A-Za-z_][A-Za-z0-9_]*$ ]] || { echo "Unsafe database name" >&2; exit 1; }

timestamp="$(date -u +%Y%m%dT%H%M%SZ)"
incoming_name="${db_name}_incoming_${timestamp}"
previous_name="${db_name}_previous_${timestamp}"
failed_name="${db_name}_failed_${timestamp}"
backup_path="$backup_dir/${db_name}-before-${timestamp}.dump"

phase="preparing"
recover_on_error() {
  local exit_code=$?
  trap - EXIT
  set +e

  if [[ "$phase" == "restoring" ]]; then
    "${compose[@]}" exec -T postgresql dropdb --if-exists --username "$db_user" "$incoming_name" || true
  elif [[ "$phase" == "swapping" ]]; then
    database_present="$("${compose[@]}" exec -T postgresql psql \
      --username "$db_user" --dbname postgres --tuples-only --no-align \
      --command "SELECT 1 FROM pg_database WHERE datname = '$db_name';")"
    previous_present="$("${compose[@]}" exec -T postgresql psql \
      --username "$db_user" --dbname postgres --tuples-only --no-align \
      --command "SELECT 1 FROM pg_database WHERE datname = '$previous_name';")"
    if [[ -z "$database_present" && "$previous_present" == "1" ]]; then
      "${compose[@]}" exec -T postgresql psql --username "$db_user" --dbname postgres \
        --command "ALTER DATABASE \"$previous_name\" RENAME TO \"$db_name\";" || true
    fi
  elif [[ "$phase" == "validating" ]]; then
    "${compose[@]}" stop api || true
    "${compose[@]}" exec -T postgresql psql --username "$db_user" --dbname postgres \
      --command "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '$db_name' AND pid <> pg_backend_pid();" \
      --command "ALTER DATABASE \"$db_name\" RENAME TO \"$failed_name\";" \
      --command "ALTER DATABASE \"$previous_name\" RENAME TO \"$db_name\";" || true
  fi

  "${compose[@]}" up --detach api web || true
  echo "Database replacement failed; the previous application database was restored when possible" >&2
  exit "$exit_code"
}

"${compose[@]}" exec -T postgresql pg_restore --list < "$dump_path" >/dev/null
install -d -m 0700 "$backup_dir"

if "${compose[@]}" --profile bot ps --status running --services | grep -qx bot; then
  echo "Refusing to replace the database while the bot is running" >&2
  exit 1
fi

"${compose[@]}" stop api
trap recover_on_error EXIT
"${compose[@]}" exec -T postgresql pg_dump \
  --format=custom --no-owner --no-privileges \
  --username "$db_user" --dbname "$db_name" > "$backup_path"
chmod 0600 "$backup_path"
"${compose[@]}" exec -T postgresql pg_restore --list < "$backup_path" >/dev/null

"${compose[@]}" exec -T postgresql createdb \
  --username "$db_user" --owner "$db_user" --template template0 "$incoming_name"

phase="restoring"

"${compose[@]}" exec -T postgresql pg_restore \
  --exit-on-error --no-owner --no-privileges \
  --username "$db_user" --dbname "$incoming_name" < "$dump_path"

phase="swapping"
"${compose[@]}" exec -T postgresql psql --username "$db_user" --dbname postgres \
  --set ON_ERROR_STOP=1 \
  --command "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '$db_name' AND pid <> pg_backend_pid();" \
  --command "ALTER DATABASE \"$db_name\" RENAME TO \"$previous_name\";" \
  --command "ALTER DATABASE \"$incoming_name\" RENAME TO \"$db_name\";"

phase="validating"
"${compose[@]}" run --rm api python manage.py migrate --noinput
"${compose[@]}" run --rm api python manage.py collectstatic --noinput
"${compose[@]}" run --rm api python manage.py check
"${compose[@]}" up --detach api web
"$repo_root/ops/oracle/verify.sh"

phase="complete"
trap - EXIT

echo "Database replacement completed"
echo "Previous database retained as: $previous_name"
echo "Pre-replacement dump written to: $backup_path"
