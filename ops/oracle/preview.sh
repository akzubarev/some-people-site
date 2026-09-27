#!/usr/bin/env bash
set -Eeuo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
compose=(docker compose
  --project-name some-people-react-preview
  -f "$repo_root/docker/docker-compose.frontend-tests.yaml"
  -f "$repo_root/docker/docker-compose.oci-preview.yaml")

usage() {
  cat <<'EOF'
Usage: ./ops/oracle/preview.sh start|status|stop
       ./ops/oracle/preview.sh restore-dump /absolute/path/to/dump --confirm-replace-preview-db

This stack is separate from production. Its web port binds to OCI localhost:5174,
its database is a preview-only Docker volume, and its API loads no production env.
Run it from a separate branch checkout, not from the live production checkout.
EOF
}

[[ $# -ge 1 ]] || { usage >&2; exit 2; }
command -v docker >/dev/null || { echo "Docker is required" >&2; exit 127; }
[[ ! -e "$repo_root/backend/.env" ]] || {
  echo "Refusing to run a preview from a checkout containing backend/.env" >&2
  exit 1
}
"${compose[@]}" config --quiet

case "$1" in
  start)
    [[ $# -eq 1 ]] || { usage >&2; exit 2; }
    "${compose[@]}" up --build --detach browser-db browser-api browser-web
    ;;
  status)
    [[ $# -eq 1 ]] || { usage >&2; exit 2; }
    "${compose[@]}" ps
    ;;
  stop)
    [[ $# -eq 1 ]] || { usage >&2; exit 2; }
    "${compose[@]}" stop browser-web browser-api browser-db
    ;;
  restore-dump)
    [[ $# -eq 3 && "$3" == --confirm-replace-preview-db ]] || { usage >&2; exit 2; }
    command -v curl >/dev/null || { echo "curl is required" >&2; exit 127; }
    dump_path="$2"
    [[ "$dump_path" == /* && -f "$dump_path" && -r "$dump_path" ]] || {
      echo "The dump must be an absolute, readable file path" >&2
      exit 2
    }
    # Validate before changing the current preview. Never inspect or print rows.
    docker run --rm --interactive --network none postgres:15 pg_restore --list \
      < "$dump_path" > /dev/null
    "${compose[@]}" stop browser-web browser-api
    "${compose[@]}" up --detach browser-db
    for _ in {1..30}; do
      if "${compose[@]}" exec -T browser-db pg_isready \
        --username security_tests --dbname security_tests > /dev/null 2>&1; then
        break
      fi
      sleep 2
    done
    "${compose[@]}" exec -T browser-db pg_isready \
      --username security_tests --dbname security_tests > /dev/null
    "${compose[@]}" exec -T browser-db dropdb \
      --if-exists --force --username security_tests security_tests
    "${compose[@]}" exec -T browser-db createdb \
      --username security_tests --owner security_tests security_tests
    "${compose[@]}" exec -T browser-db pg_restore \
      --exit-on-error --no-owner --no-privileges \
      --username security_tests --dbname security_tests < "$dump_path"
    "${compose[@]}" up --build --detach browser-api browser-web
    for _ in {1..30}; do
      if curl --fail --silent http://127.0.0.1:5174/api/games/ > /dev/null; then
        echo "Preview restored and serving on OCI localhost:5174"
        exit 0
      fi
      sleep 2
    done
    echo "Preview API did not become ready" >&2
    exit 1
    ;;
  *)
    usage >&2
    exit 2
    ;;
esac
