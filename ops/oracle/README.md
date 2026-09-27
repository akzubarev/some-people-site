# OCI operations

The public site runs on an Oracle ARM64 VM. Host nginx terminates TLS and
proxies to the production Compose web container on `127.0.0.1:8080`. The
default production project is `some-people-prod`: PostgreSQL, Django API, and
React web. The Telegram bot is an explicit `bot` profile, not part of normal
deployment. Do not infer the VM's current bot or backup-timer state from the
repository; verify it before operating.

Production operations need authorization and the host's existing credentials.
Never copy `backend/.env`, database dumps, or private media into a branch
checkout or commit them.

## Deploy and verify

Run from a clean, authorized production checkout after identifying the intended
Git commit. `backend/.env` must exist on the VM without exposing its values;
Docker, curl, and the Ubuntu `acl` package are required.

```bash
docker compose -f docker/docker-compose.prod.yaml config --quiet
bash ops/oracle/deploy.sh
bash ops/oracle/verify.sh --expect-bot-stopped
```

`deploy.sh` builds API and web images, starts PostgreSQL, applies migrations,
collects static files, runs Django checks, starts API/web, grants the nginx
worker narrow access to admin static files, and smoke-tests localhost routes.
It neither restores a database nor starts the bot unless separately directed.
`verify.sh` reports HTTP/container status, aggregate data counts, migration
consistency, and the requested bot state. For an intentionally running bot, use
`--expect-bot-running`.

`docker/nginx/oci.conf` serves the React SPA and proxies Django routes,
including `/api/`, `/admin/`, and `/ckeditor/`. The host configuration is
`somepeoplelarp.ru.public.conf`; check public HTTPS separately after deploy.
Do not use the optional `--restore` or `replace-database.sh` path as a normal
deployment step.

## Isolated branch previews

Use a separate checkout of the branch under test with **no**
`backend/.env`. The preview project `some-people-react-preview` has its own
PostgreSQL volume and binds its web service only to OCI localhost port 5174;
it does not replace production containers or the production database.

```bash
bash ops/oracle/preview.sh start
bash ops/oracle/preview.sh status
bash ops/oracle/preview.sh stop
```

The overlay is `docker/docker-compose.oci-preview.yaml` on top of
`docker/docker-compose.frontend-tests.yaml`. The latter's ordinary browser
test stack is synthetic and ephemeral; the overlay makes the preview database
persistent and uses `config.preview_settings` so restored production password
hashes work without loading production secrets. An authorized, isolated dump
restore requires an absolute archive path and
`restore-dump /absolute/path --confirm-replace-preview-db`. It replaces only
the preview database after archive validation. Reach the preview through an
SSH localhost tunnel rather than exposing port 5174 publicly.

## Media and backups

Production can use OCI Object Storage for uploaded media. Before changing
`MEDIA_STORAGE` or deleting local media, use the repository's
`copy_media_to_s3` verification flow and
`activate-media-s3.sh --confirm-verified-copy` only as an authorized media
migration. Raw legacy `/media/` links may still require local files; inspect
their usage before cleanup. `sync-media.sh` is retained for resumable
filesystem transfers.

`backup-database.sh --upload` can create a validated custom-format PostgreSQL
dump and upload it to the private Object Storage bucket with a readback hash
check. The provided systemd service/timer is optional; do not assume it is
enabled. The script does not prune old backups. Retain independent credentials
and test a restore before relying on any backup.

## Historical cutover tools

`create-env.sh`, `configure-https-env.sh`,
`activate-public-nginx.sh`, `replace-database.sh`, and the pre-cutover nginx
configuration were used to prepare and switch from Yandex to OCI. They remain
for recovery or another explicitly authorized migration, not for routine
deploys. `docker.sources`, `docker-daemon.json`, and `journald.conf` document
the VM's Docker and log configuration. Avoid enabling HSTS or re-running a
database replacement as an incidental check.
