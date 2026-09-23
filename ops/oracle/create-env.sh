#!/usr/bin/env bash
set -Eeuo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
env_file="$repo_root/backend/.env"

[[ ! -e "$env_file" ]] || {
  echo "Refusing to overwrite existing $env_file" >&2
  exit 1
}

command -v openssl >/dev/null 2>&1 || { echo "openssl is required" >&2; exit 127; }

umask 077
db_password="$(openssl rand -hex 32)"
django_secret="$(openssl rand -hex 48)"

cat > "$env_file" <<EOF
DEBUG=0
POSTGRES_USER=somepeople
POSTGRES_PORT=5432
POSTGRES_DB=somepeople
POSTGRES_PASSWORD=$db_password
POSTGRES_HOST=postgresql

SECRET_KEY=$django_secret
DOMAINS=somepeoplelarp.ru,89.168.92.43,localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=https://somepeoplelarp.ru,http://127.0.0.1:8080
CSRF_COOKIE_SECURE=1
SESSION_COOKIE_SECURE=1
TRUST_X_FORWARDED_PROTO=1
# Enable only when the public TLS reverse proxy is active.
SECURE_SSL_REDIRECT=0
SECURE_HSTS_SECONDS=0
SECURE_HSTS_INCLUDE_SUBDOMAINS=0
SECURE_HSTS_PRELOAD=0
API_URL=http://api:8000

TELEGRAM_BOT_TOKEN=
TELEGRAM_BOT_USERNAME=
TELEGRAM_BOT_ADMIN_IDS=

CELERY_BROKER_URL=
CELERY_RESULT_BACKEND=

MAIN_SITE_ID=1
COMPANY_ID=1
TIME_ZONE=Europe/Moscow
EOF

chmod 0600 "$env_file"
echo "Created $env_file with OCI-local secrets"
