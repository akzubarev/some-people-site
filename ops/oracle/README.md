# Oracle VM deployment and pre-cutover configuration

These files prepare the Oracle ARM64 host and provide a guarded deployment path.

- `docker.sources` configures Docker's official Ubuntu 26.04 ARM64 repository.
- `docker-daemon.json` bounds Docker JSON logs and enables live restore.
- `journald.conf` bounds persistent and runtime system journals.
- `somepeoplelarp.ru.pre-cutover.conf` is staged in nginx `sites-available` but
  must not be enabled until a separately authorized cutover.
- `somepeoplelarp.ru.public.conf` is the final TLS reverse proxy. It forwards
  the original HTTPS scheme through the frontend proxy to Django.
- `activate-public-nginx.sh` refuses to run without both an explicit cutover
  flag and an existing Let's Encrypt certificate.
- `configure-https-env.sh prepare` enables secure cookies and proxy awareness
  without redirecting HTTP. Run its `activate` mode only with the public TLS
  proxy ready.
- `deploy.sh` validates and builds the production Compose stack, optionally
  restores a custom-format dump into an empty database, runs migrations and
  `collectstatic`, and smoke-tests the localhost-only web endpoint. It grants
  the nginx worker a narrow ACL on the static root so admin CSS is readable.
- `replace-database.sh` performs the final, explicitly confirmed database
  replacement through a restored temporary database. It retains both the
  previous database and a custom-format backup for rollback.
- `sync-media.sh` runs from WSL and copies media through a resumable local
  cache without deleting files from either host.
- `activate-media-s3.sh` changes the production media backend only after the
  repository's `copy_media_to_s3 --apply` command has copied and verified every
  file. It retains the filesystem media and backs up the previous environment.
- `backup-database.sh --upload` creates and validates a local custom-format
  PostgreSQL dump, uploads it under `database-backups/` in the private OCI
  Object Storage bucket, and reads it back to verify the SHA-256 digest. The
  systemd timer runs it daily; no backups are pruned automatically.
- `create-env.sh` creates an OCI-local production environment file with fresh
  database and Django secrets. It refuses to overwrite an existing file and
  leaves Telegram credentials empty.
- `verify.sh` reports container and HTTP health, checks the requested bot
  state (`--expect-bot-stopped` by default, or `--expect-bot-running`), prints
  aggregate restored-data counts, and checks migrations.

The default Compose stack starts PostgreSQL, the Django API, and the static web
container. The web endpoint binds only to `127.0.0.1:8080`. The Telegram bot is
behind the explicit `bot` profile and is not started by `deploy.sh`.
Install the Ubuntu `acl` package before deploying; static files are readable
only to the frontend nginx worker, not to every local account.

## Preparation sequence

1. Run `configure-https-env.sh prepare`, redeploy, and verify the private stack.
2. Run `sync-media.sh` for the initial media copy; repeat it in the write-free
   cutover window for the final incremental copy.
3. Obtain a certificate using DNS validation while DNS still points at Yandex,
   or enable the pre-cutover HTTP site after the A-record switch and use the
   ACME webroot `/var/www/certbot`.
4. In the maintenance window, stop all Yandex writers and its bot, create a
   fresh dump, then run `replace-database.sh` with its confirmation flag.
5. Run `configure-https-env.sh activate`, deploy, and invoke
   `activate-public-nginx.sh --confirm-public-cutover`.

Do not enable HSTS during the initial cutover. Set a short value only after TLS
and rollback behavior have been observed, then increase it separately.

The DNS change and bot startup remain separately authorized cutover operations.
The frontend slimming and optional OCI Object Storage backend are now merged.
After the final media sync, configure `MEDIA_S3_*`, run
`docker compose -f docker/docker-compose.prod.yaml run --rm --no-deps
-e MEDIA_STORAGE=s3 api python manage.py copy_media_to_s3 --apply`, check that
every file is copied or identical with zero pending, then run
`activate-media-s3.sh --confirm-verified-copy` and `deploy.sh`. Before removing
the VM's local media copy, run `copy_media_to_s3` again without `--apply` and
require every file to be identical with zero pending. Retain an independent
copy for rollback. Raw legacy `/media/` URLs are not rewritten to signed S3
URLs and may stop working after local media cleanup; database content should
be checked for such links first.

To enable daily off-VM database backups after verifying Object Storage access:

```bash
sudo install -m 0644 ops/oracle/some-people-database-backup.service /etc/systemd/system/
sudo install -m 0644 ops/oracle/some-people-database-backup.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start some-people-database-backup.service
sudo systemctl enable --now some-people-database-backup.timer
```

Keep an independent copy of backup credentials and periodically test a restore.
