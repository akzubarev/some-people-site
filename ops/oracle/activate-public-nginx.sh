#!/usr/bin/env bash
set -Eeuo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
site_name="somepeoplelarp.ru"
source_config="$repo_root/ops/oracle/$site_name.public.conf"
available_config="/etc/nginx/sites-available/$site_name"
enabled_config="/etc/nginx/sites-enabled/$site_name"
certificate_dir="/etc/letsencrypt/live/$site_name"

[[ "${1:-}" == "--confirm-public-cutover" ]] || {
  echo "Usage: sudo $0 --confirm-public-cutover" >&2
  echo "Refusing to expose the site without the explicit cutover flag." >&2
  exit 2
}

[[ $EUID -eq 0 ]] || { echo "Run this script with sudo" >&2; exit 1; }
command -v nginx >/dev/null 2>&1 || { echo "nginx is required" >&2; exit 127; }
[[ -f "$source_config" ]] || { echo "Missing $source_config" >&2; exit 1; }
[[ -s "$certificate_dir/fullchain.pem" ]] || { echo "Missing TLS certificate" >&2; exit 1; }
[[ -s "$certificate_dir/privkey.pem" ]] || { echo "Missing TLS private key" >&2; exit 1; }

# Certbot's webroot authenticator does not install the nginx plugin defaults.
if [[ ! -s /etc/letsencrypt/options-ssl-nginx.conf ]]; then
  packaged_options=/usr/lib/python3/dist-packages/certbot_nginx/_internal/tls_configs/options-ssl-nginx.conf
  [[ -s "$packaged_options" ]] || { echo "Missing packaged Certbot nginx TLS options" >&2; exit 1; }
  install -m 0644 "$packaged_options" /etc/letsencrypt/options-ssl-nginx.conf
fi
if [[ ! -s /etc/letsencrypt/ssl-dhparams.pem ]]; then
  packaged_dhparams=/usr/lib/python3/dist-packages/certbot/ssl-dhparams.pem
  [[ -s "$packaged_dhparams" ]] || { echo "Missing packaged Certbot DH parameters" >&2; exit 1; }
  install -m 0644 "$packaged_dhparams" /etc/letsencrypt/ssl-dhparams.pem
fi
[[ -s /etc/letsencrypt/options-ssl-nginx.conf ]] || { echo "Missing Certbot TLS options" >&2; exit 1; }
[[ -s /etc/letsencrypt/ssl-dhparams.pem ]] || { echo "Missing Certbot DH parameters" >&2; exit 1; }

install -d -m 0755 /var/www/certbot
install -m 0644 "$source_config" "$available_config"
ln -sfn "$available_config" "$enabled_config"

nginx -t
systemctl enable --now nginx
systemctl reload nginx

curl --fail --silent --show-error \
  --resolve "$site_name:443:127.0.0.1" \
  "https://$site_name/healthz" >/dev/null

echo "$site_name is available through the local TLS reverse proxy"
