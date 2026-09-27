# Some People

Some People is a website for a live-action role-playing community. It connects game announcements and character selection with player applications, questionnaires, and communication with the organizing team. The interface is in Russian.

## What the application does

Visitors can read about games and browse published characters by faction, family, or tag. Registered players can save characters they are interested in, apply to a game, complete its questionnaire, and follow their application status in their personal account.

Organizers manage games, role visibility, character assignments, application decisions, participation fees, and mailings through Django admin. Players can connect Telegram to receive messages from the organizers.

## How it fits together

The React interface handles navigation, forms, and display. A Django REST API validates requests, controls access, and stores the application's records in PostgreSQL. Uploaded images and files use either filesystem storage or private S3-compatible object storage. A separate Telegram bot connects player accounts and delivers scheduled messages.

| Part | Responsibility |
| --- | --- |
| React, TypeScript, React Router | Game pages, role grid, personal account, forms |
| Django REST Framework | Application rules, authentication, API, validation |
| Django admin | Organizer-facing content and application management |
| PostgreSQL | Players, games, roles, applications, answers, mailings |
| Media storage | Avatars, portraits, character files, rich-text uploads |
| Telegram bot | Account linking and notification delivery |

## Documentation

- [Application behavior](docs/application.md): games and role visibility, the application lifecycle, questionnaires, profiles, and organizer workflows.
- [Architecture](docs/architecture.md): domain relationships, request and data flow, sessions, API contracts, caching, media, and Telegram integration.
