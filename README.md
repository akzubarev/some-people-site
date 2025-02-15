# some-people-site

Website for LARP community to help register and follow the MG "Some-people"

# Aliases

- `dcu` - `docker compose up`
- `dce` - `docker exec -it`
- `dcd` - `docker compose down --remove-orphans`

# startup

- Copy `backend/example.env` to `backend/.env`, change accordingly
- `ln -s docker/docker-compose.prod.yaml docker/docker-compose.yaml`
- `sh pre-startup.sh`
- `dcu`
- `dce api sh startup.sh`
- `dc run builder.frontend yarn`
- `dc run builder.frontend`

## stop

- `dcd`

# dev

- traefik: http://localhost:9090/dashboard/#/
- admin: http://v1.admin.some-people.localhost:1337/admin
- app: http://v1.app.some-people.localhost:1337/

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