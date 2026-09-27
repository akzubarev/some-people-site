# Some People project index

Some People is a LARP-community application: Django 5.1 and Django REST
Framework, a React 19/TypeScript SPA built with Vite and pnpm, PostgreSQL 15,
and an opt-in Telegram bot. Develop through Docker Compose in WSL. The public
deployment runs on an OCI VM; production changes require explicit authorization.

## Repository map

- `backend/`: Django API, admin, models, migrations, bot, and tests.
- `frontend/`: React SPA, generated API types, unit and Playwright tests.
- `docker/`: explicit development, test, preview, and production Compose files,
  images, and nginx configuration.
- `scripts/project.sh`: local Compose helper.
- `ops/oracle/`: OCI deployment, verification, preview, media, and backup tools.
- `.agents/skills/some-people-development/`: project-specific agent guidance.

Read the nearest nested `AGENTS.md` before changing backend or frontend code.
Use `README.md` for setup and `ops/oracle/README.md` for OCI operations.

## Local workflow

Run from the repository root inside WSL. Confirm `backend/.env` exists without
printing it; copy `backend/example.env` and fill local values on first use.

```bash
./scripts/project.sh dev up
./scripts/project.sh dev migrate
./scripts/project.sh dev check
```

The app is at `http://v1.app.some-people.localhost:1886/`, admin at
`http://v1.admin.some-people.localhost:1886/admin/`, and Traefik at
`http://localhost:9090/dashboard/`. Run `./scripts/project.sh help` for
other commands.

## Change discipline

- Name new feature branches `feature/<short-description>`. Keep temporary
  workplans and screenshots in the ignored `refactoring-workplans/` directory.
- Version maintained documentation and agent instructions with the code they
  describe. Update the existing authoritative guide; do not create duplicate
  guides. Include documentation impact in PR descriptions.
- Keep Django API serializers/views, generated `backend/openapi.yaml`, and
  generated `frontend/src/shared/api/schema.ts` synchronized.
- Add new Django migrations for schema changes; do not rewrite applied ones.
- Use focused checks: Django system/migration checks and relevant tests for
  backend changes; typecheck, lint, unit tests, and build for frontend changes.
  CI also runs browser checks. Report exactly what was run.
- Do not commit `backend/.env`, credentials, database contents or dumps,
  generated `frontend/dist`, or runtime media.
- Treat production Compose, nginx, environment handling, database restore,
  media storage, and bot startup as deployment-sensitive. The bot is opt-in
  through a Compose profile. Never deploy, restore data, or alter OCI/Yandex
  resources without authorization for that operation.

## Documentation maintenance

Check code and executable configuration before documenting behavior. Distinguish
merged production behavior from branch previews. Keep the root README as the
entry point and link focused guides. Regenerate API contracts instead of
hand-editing generated files. Validate documented commands and relative links.
Never put secrets, private data, or temporary troubleshooting output in docs.
