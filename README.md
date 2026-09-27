# Some People

A LARP-community website with a Django REST API and admin, a React/TypeScript
SPA, PostgreSQL, and an optional Telegram bot. The frontend uses Vite and pnpm.
The public deployment is hosted on an OCI VM at
[somepeoplelarp.ru](https://somepeoplelarp.ru/).

## Local development

Use WSL with Docker integration enabled. From the repository root, copy
`backend/example.env` to `backend/.env` on first use and fill in local
values. Never commit the resulting environment file.

```bash
./scripts/project.sh dev up
./scripts/project.sh dev migrate
./scripts/project.sh dev check
```

- App: http://v1.app.some-people.localhost:1886/
- Admin: http://v1.admin.some-people.localhost:1886/admin/
- Traefik dashboard: http://localhost:9090/dashboard/

`./scripts/project.sh help` lists the other explicit Compose commands.
Frontend scripts are in `frontend/package.json`; use Node 22.23.2 and pnpm
12.5.1 when running them outside Docker.

## Verification and API contracts

- Django checks: `./scripts/project.sh dev check` and
  `./scripts/project.sh dev migrations-check`.
- Frontend: `./scripts/project.sh dev typecheck` and
  `./scripts/project.sh dev frontend-build`; `pnpm lint`, `pnpm test`,
  and `pnpm test:e2e` are also available in `frontend/`.
- The full PostgreSQL, OpenAPI, frontend, and browser checks run in
  [CI](.github/workflows/checks.yml).

The API lives under `/api/`. Django generates
[`backend/openapi.yaml`](backend/openapi.yaml), exposed through
`/api/schema/` and `/api/docs/`; the frontend generates its types from that
file with `pnpm api:generate`.

## OCI operations

Production uses [`docker/docker-compose.prod.yaml`](docker/docker-compose.prod.yaml):
PostgreSQL, API, and web are started by default; the Telegram bot requires the
explicit `bot` profile. The web container listens on OCI localhost port 8080
behind the host's TLS reverse proxy.

See [`ops/oracle/README.md`](ops/oracle/README.md) for deployment, verification,
media storage, backups, and the isolated branch-preview workflow. Production
deployment, database restoration, and bot startup are separate authorized
operations; local development commands are not substitutes for that runbook.
