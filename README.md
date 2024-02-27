# some-people-site
Website for LARP community to help register and follow the MG "Some-people"
Frontend is done on Vue.js with typescript
Backend is done with Python Django and DRF
Conteinerized with Docker by docker-compose configs

# Main Functionality

## Display team info and short description of current and future projects
- / -> About.vue
- /games -> Games.vue

## Display further info about indiviluad games, the roles list and conditions of applying
- /games/<game>/about -> game/About.vue
- /games/<game>/roles -> game/Roles.vue

## Take apllications, decline or approve them, assign users to roles
- /games/<game>/apply -> game/Application.vue

## Allow users to edit their personal information, delete their applications
- /profile -> Profile.vue
- /profile/settings -> Settings.vue

# Admin functionality (Default Django admin with a few extensions)
- create/edit/delete all information about games, chracters and fractions
