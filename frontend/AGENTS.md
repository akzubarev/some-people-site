# Frontend index

`frontend/` is a React 19/TypeScript SPA using React Router, Vite, and pnpm
with Node 22.23.2. It is not a Vue/Vuex or Yarn project.

## Map

- `src/main.tsx`, `src/app/Shell.tsx`, and `src/app/router.tsx`: bootstrap,
  shell, routes, loaders, and actions.
- `src/app/data.ts`: route data loading and mutations.
- `src/features/`: games, auth, and account screens.
- `src/shared/api/client.ts`: same-origin Django API client.
- `src/shared/api/schema.ts`: generated types from `backend/openapi.yaml`;
  regenerate via `pnpm api:generate`, do not hand-edit.
- `src/shared/styles.css` and `src/assets/`: preserved visual design.
- `tests/`: Playwright browser tests; `src/**/*.test.*`: unit tests.

When changing an API contract, update Django and generated types together.
Keep session authentication and CSRF behavior intact; the browser uses Django
sessions. Preserve route navigation, form persistence, and responsive layouts.

From WSL, use `./scripts/project.sh dev typecheck` and
`./scripts/project.sh dev frontend-build`. In a Node 22.23.2/pnpm 12.5.1
environment, `pnpm lint`, `pnpm test`, `pnpm test:e2e`, and
`pnpm api:check` provide focused checks. The full CI browser suite also
starts a synthetic Django stack; do not run live-data tests against production.
