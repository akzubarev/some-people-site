#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

usage() {
  cat <<'EOF'
Usage: ./scripts/project.sh <dev|prod> <command> [args...]

Commands:
  up                 Build and start the selected stack in the background
  down               Stop the selected stack and remove orphan containers
  ps                 Show service status
  logs [service]     Follow logs for all services or one service
  build [service]    Build all images or one service
  django <args...>   Run a Django management command in the API service
  migrate            Apply Django migrations
  migrations-check  Fail if model changes need migrations
  check              Run Django's system checks
  shell              Open a shell in the API service
  typecheck          Run the frontend TypeScript compiler without emitting
  frontend-build     Run the frontend production build

Production commands target the OCI-compatible Compose definition. The default
production stack excludes the Telegram bot; it is available only through the
explicit Compose profile named "bot". Use ops/oracle/deploy.sh for the guarded
pre-cutover build, optional empty-database restore, migrations, and smoke test.
EOF
}

if [[ $# -lt 2 || "${1:-}" == "help" || "${2:-}" == "help" ]]; then
  usage
  exit 0
fi

environment="$1"
command="$2"
shift 2

case "$environment" in
  dev) compose_file="$repo_root/docker/docker-compose.dev.yaml" ;;
  prod) compose_file="$repo_root/docker/docker-compose.prod.yaml" ;;
  *) echo "Unknown environment: $environment" >&2; usage >&2; exit 2 ;;
esac

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker is not available. Run this helper inside WSL with Docker integration enabled." >&2
  exit 127
fi

compose=(docker compose --project-directory "$repo_root/docker" -f "$compose_file")

case "$command" in
  up) "${compose[@]}" up --build -d "$@" ;;
  down) "${compose[@]}" down --remove-orphans "$@" ;;
  ps) "${compose[@]}" ps "$@" ;;
  logs) "${compose[@]}" logs --follow "$@" ;;
  build) "${compose[@]}" build "$@" ;;
  django)
    [[ $# -gt 0 ]] || { echo "django requires a management command" >&2; exit 2; }
    "${compose[@]}" exec api python manage.py "$@"
    ;;
  migrate) "${compose[@]}" exec api python manage.py migrate "$@" ;;
  migrations-check) "${compose[@]}" exec api python manage.py makemigrations --check --dry-run "$@" ;;
  check) "${compose[@]}" exec api python manage.py check "$@" ;;
  shell) "${compose[@]}" exec api sh "$@" ;;
  typecheck)
    [[ "$environment" == "dev" ]] || { echo "typecheck is available only in dev" >&2; exit 2; }
    "${compose[@]}" exec app yarn tsc --noEmit "$@"
    ;;
  frontend-build)
    if [[ "$environment" == "dev" ]]; then
      "${compose[@]}" exec app yarn build "$@"
    else
      "${compose[@]}" build web "$@"
    fi
    ;;
  *) echo "Unknown command: $command" >&2; usage >&2; exit 2 ;;
esac
