# Backend index

`backend/` is the Django 5.1/DRF application. `config/settings.py` owns
environment, PostgreSQL, static/media, security, and Telegram settings.
Domain code lives in `apps/users`, `apps/games`, and `apps/notifications`;
`bot/` uses Django models directly. The custom user model is `users.User`.

## Follow a change

- Trace models, serializers, views, URLs, tests, and bot imports when changing
  an API field or behavior. Browser session endpoints live under `/api/`;
  token endpoints remain for other clients.
- For schema changes, add a migration. Do not edit an applied migration.
- `config/urls.py` serves generated schema and Swagger at `/api/schema/`
  and `/api/docs/`. Regenerate `backend/openapi.yaml` and the frontend
  contract when serializers or routes change.
- Production media may use OCI Object Storage; preserve the selected storage
  backend and never assume local media files contain the complete library.
- Add environment variable names to `example.env` using placeholders only.

## Checks

From WSL, use `./scripts/project.sh dev check` and
`./scripts/project.sh dev migrations-check`. The PostgreSQL regression suite
is run by `docker compose -f docker/docker-compose.security-tests.yaml run
--build --rm tests`; see `.github/workflows/checks.yml` for the full CI
sequence and OpenAPI consistency check. Report the actual checks run.

Never print `.env`, credentials, database contents, or dumps. Do not run
fixtures, one-off scripts, production Compose, or restore commands as incidental
validation.
