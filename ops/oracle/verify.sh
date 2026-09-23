#!/usr/bin/env bash
set -Eeuo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
compose_file="$repo_root/docker/docker-compose.prod.yaml"
compose=(docker compose -f "$compose_file")
expected_bot="${1:---expect-bot-stopped}"

[[ "$expected_bot" == "--expect-bot-stopped" || "$expected_bot" == "--expect-bot-running" ]] || {
  echo "Usage: $0 [--expect-bot-stopped|--expect-bot-running]" >&2
  exit 2
}

"${compose[@]}" ps

for path in /healthz / /admin/ /api/games/; do
  status="$(curl --silent --output /dev/null --write-out '%{http_code}' "http://127.0.0.1:8080$path")"
  printf '%s %s\n' "$status" "$path"
done

if "${compose[@]}" --profile bot ps --status running --services | grep -qx bot; then
  actual_bot="running"
else
  actual_bot="stopped"
fi
if [[ "$expected_bot" != "--expect-bot-$actual_bot" ]]; then
  echo "Bot is $actual_bot, expected ${expected_bot#--expect-bot-}" >&2
  exit 1
fi
echo "bot $actual_bot"

db_user="$("${compose[@]}" exec -T postgresql printenv POSTGRES_USER)"
db_name="$("${compose[@]}" exec -T postgresql printenv POSTGRES_DB)"

for table in users_user games_game games_character games_application; do
  count="$("${compose[@]}" exec -T postgresql psql \
    --username "$db_user" \
    --dbname "$db_name" \
    --tuples-only \
    --no-align \
    --command "SELECT count(*) FROM $table;")"
  printf '%s=%s\n' "$table" "$count"
done

database_size="$("${compose[@]}" exec -T postgresql psql \
  --username "$db_user" \
  --dbname "$db_name" \
  --tuples-only \
  --no-align \
  --command 'SELECT pg_size_pretty(pg_database_size(current_database()));')"
printf 'database_size=%s\n' "$database_size"

"${compose[@]}" run --rm api python manage.py migrate --check
