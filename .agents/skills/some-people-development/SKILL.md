---
name: some-people-development
description: Develop, diagnose, review, or operate the Some People Django/React application and its Docker/OCI workflows. Use only within this repository.
---

# Some People development

Read the root `AGENTS.md` and the nearest nested `AGENTS.md` before changing
code. Use `rg` to trace a feature rather than assuming framework defaults.
`README.md` is the setup entry point; `ops/oracle/README.md` is the OCI
operations guide.

## Choose the change surface

- Backend/API: trace model, serializer, view, route, migration, tests, and bot
  imports. Keep `backend/openapi.yaml` and generated frontend API types aligned.
- Frontend: trace React Router loader/action, feature component, shared API
  client, styles, and browser/unit tests. Preserve Django session/CSRF behavior.
- Runtime: inspect the explicit Compose file and relevant Dockerfile. Local
  development runs in WSL with Docker integration.
- OCI: production and the branch-preview stack are separate Compose projects.
  The preview uses its own PostgreSQL volume and must not have `backend/.env`;
  see `ops/oracle/preview.sh`. The production bot is an opt-in profile.

## Verify proportionally

Prefer `scripts/project.sh` for local Compose commands. Confirm
`backend/.env` exists without displaying values before starting local
containers. Run Django checks and relevant tests for backend changes;
typecheck, lint, unit/browser tests, and build for frontend changes. Run
`docker compose -f <file> config --quiet` before relying on changed Compose
definitions. Report exact checks, not assumed coverage.

Never expose credentials, dumps, or private data. Do not deploy, restore a
database, migrate media, or start the bot as incidental validation; obtain
authorization for the specific production action. Update maintained project
docs and agent guidance with behavior-changing code, keeping temporary notes
in ignored `refactoring-workplans/`.
