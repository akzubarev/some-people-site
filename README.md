# some-people-site

Website for LARP community to help register and follow the MG "Some-people"

# Local development

Run the project helper from WSL. On first use, copy `backend/example.env` to
`backend/.env` and fill in local values. Do not commit that file.

```bash
./scripts/project.sh dev up
./scripts/project.sh dev migrate
./scripts/project.sh dev check
```

Use `./scripts/project.sh help` for the other commands. The frontend is React
and Vite, with dependencies managed by pnpm.

# dev

- traefik: http://localhost:9090/dashboard/#/
- admin: http://v1.admin.some-people.localhost:1886/admin
- app: http://v1.app.some-people.localhost:1886/

# prod

## app: http://{domain}/

- `/` - main page
- `/mg` - list of the master group
- `/games` - games list with short info
    - `/<alias>`
        - `/about` - more info about the game
        - `/roles` - roles list for the game
        - `/apply` - application for the game
- `/account`
    - `/profile` - users profile
    - `/settings` - user settings
    - `/telegram` - telegram account linking
    - `/notifications` - notifications list

## api

- `/auth/me/` - authorization
- `/games` - games list
    - `games/<alias>` - game info
    - `/characters/` - game characters
    - `tags` - tags for the characters and groups
    - `/questions/` - questions for the application
    - `/applications` - game applications
        - `/get/` - get one application
        - `/apply/` - create application
- `/users` - users list
    - `/mg` - list of master group
    - `/users/{user_id}` - one user
    - `/players` - list of players for the game
    - `/telegram` - create telegram link code

## admin: http://<domain>/admin
