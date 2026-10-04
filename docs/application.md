# Application behavior

## Games and the role grid

A game has a description, location, dates, participation fee, and links to its communities. Publication of its role grid and acceptance of new applications are controlled separately. A game can therefore publish its characters before applications open, or keep its role grid available after registration closes.

Characters are organized into factions and families. Groups can contain subgroups, producing a hierarchy in the role-grid navigation. A character belongs to a faction and can also belong to a family. Tags provide another way to find characters through the searchable character list.

Hidden groups are excluded from public results along with their descendants. A character is publicly visible only when its faction and any associated family are visible. This rule applies to the API response, so hidden content is not merely concealed by the page layout.

Character cards show the portrait, name, description, and assigned player when present. A game-specific image fills in for a missing or failed portrait. Clicking a group title takes the reader to its section; the separate disclosure control expands or collapses its navigation children.

For current or future games, unassigned characters show a vacancy label and a heart. A signed-in player's heart records interest in a character; it does not reserve the role or assign it to that player. Once a game's end date has passed, those vacancy labels and hearts disappear. If there is no valid end date, an earlier game year is used instead. Assigned player names remain visible for past games.

## Applying to a game

Registration signs the player in. If they reached registration or sign-in from a protected page, they return to that page afterward, preserving the selected game.

The personal account contains the selected game's application and questionnaire, with profile settings in the same layout. Before applying, it shows either the application button or a message that registration is closed.

Submitting creates the player's application for that game with status `pending`. Subsequent saves update the existing application and its answers. The API identifies the player from the authenticated session; an application request does not choose another player's account.

| Status | Meaning in the account |
| --- | --- |
| `pending` | Submitted |
| `discussing` | Under discussion |
| `confirmed` | Accepted |
| `declined` | Declined |
| `deleted` | Withdrawn by the player |

Organizers manage decisions and character assignments in admin. An application can have one assigned character, and a character can be assigned to at most one application. Likes remain separate from this assignment.

The account displays the assigned character, questionnaire completion, and participation fee information. The fee is copied from the game when the application is created; the application also records the amount paid. These are displayed records, not an online payment checkout.

Deleting an application changes its status to `deleted` rather than removing its record and answers. The player can restore it, which returns its status to `pending`. Editing answers on a deleted application requires restoring it first. Closing new applications does not erase existing applications or their saved answers.

## Questions and saved answers

Questions are associated with games and can be reused across them. Each question has an ordering value, a required flag, a field type, and any available choices. The application page displays questions with negative order values as additional information; the separate questionnaire displays its questionnaire fields.

The supported fields are a short line, a paragraph, one choice, multiple choices, a scale, a matrix with one choice per row, and a matrix with multiple choices per row. Answers belong to an application and a question. The backend validates that submitted questions belong to the game and that the values match their field types.

Answers save automatically. The interface serializes requests so that an earlier save cannot overwrite a later edit through out-of-order completion. It shows pending and saved states, retains edits after a failed save, and offers a retry. Navigation protection warns about unsaved work. Required answers that are missing or incomplete contribute to the account's questionnaire completion indicator.

## Profiles and Telegram

Profile settings contain the player's name, nickname, phone, VK link, avatar, and public social-link preferences. Email is displayed as read-only. Changes are saved explicitly. Public role cards receive a limited player representation; private profile details such as the phone number are not included. Social links are shown according to the player's visibility choices.

Choosing an avatar opens a crop dialog. Dragging and zooming choose the visible area; Apply produces the new preview, and Cancel leaves the previous selection intact. The image is uploaded when the profile is saved.

Telegram connection begins in settings. The application issues a link that can be opened or copied and expires after ten minutes. Opening it and starting the bot associates the private Telegram chat with the player's account. The code is single-use; issuing a link by itself does not complete the connection.

## Organizer workflows and messages

The MG navigation opens an organizer cabinet with a dark theme across its navigation, content editors, questionnaire controls and confirmation dialogs. Its game editor contains the title, URL alias, full and short descriptions, location, dates, year, player capacity, default fee, social links, and separate switches for accepting applications and publishing the role grid. Dates are shown in the application's configured time zone. Organizer routes identify games by their stable database ID, so the editor remains reachable after an alias change; public game links use the alias and must be updated when it changes.

Access requires an active staff or superuser account and the corresponding Django game permissions. View permission allows reading; change permission allows editing and reading; add permission allows creation. New games start with applications and the role grid closed, and can be opened in a subsequent save. Changing a game's default fee does not rewrite fees on existing applications. The organizer capacity field is the stored game value; the public API's player count continues to describe visible characters.

Saving checks the version originally loaded by the editor. If another edit has changed the game, the server rejects the stale save, and the browser retains the draft so the organizer can review it before loading current data. Navigation warns about unsaved changes. Creation and changes are recorded in Django's admin history; public game caches are invalidated after commit. Aliases are unique without regard to letter case.

The cabinet includes groups and families, character content, shared tags, questionnaires, applications, contributions, mailings and an overview. Each section requires its own Django model permissions in addition to access to the game cabinet. Group parents must belong to the same game and have the same family/faction type; cycles are rejected. Hiding a group affects its descendants in the public role grid, without discarding assignments. Groups with children or characters cannot be deleted.

The character editor owns names, alias, description, order, faction, family, master, portrait, PDF and tags. Player assignment is a secondary link to the application. A character must have a faction or family in the selected game. Assigned or liked characters are protected from deletion. Tags are shared across games; editing a tag used elsewhere requires acknowledgement.

Question options use separate inputs, scales use editable ticks, and matrices have editable row and column headings with answer-cell previews. Options can be added, removed and reordered; the question order field controls questionnaire placement. Negative order values identify application-time questions. A question shared by several games requires acknowledgement before editing. Once answers exist, its type and choices are protected; a game with answers cannot be removed from that question. Wording, required status and order can still change. Questions with answers or other game associations cannot be deleted.

Application detail combines answers, missing required questions, liked characters, status and assignment. Assignment is restricted to an unoccupied character in the same game and does not implicitly accept an application. Contributions edit the same application's fee and paid amount, with nonnegative amounts and a required reason recorded in admin history. No payment processor or transaction ledger is involved. The overview and mailing recipient filters use those same application records.

A mailing belongs to one game and contains HTML text, a scheduled time and selected application IDs. Saving creates or updates a draft; it creates no notifications. Recipient preview excludes deleted applications, inactive accounts and accounts without a linked Telegram chat. An empty selection sends to nobody. Confirmation is a separate action that checks the preview snapshot, freezes the eligible users and creates notification records in one transaction. Repeating the same confirmation key returns the existing result. Confirmed mailings are immutable; further messages require a new draft. Older mailings without a game remain visible in Django admin as read-only records.

Mailing composition uses a self-hosted Tiptap editor inside the cabinet, loaded only when needed. It supports formatted text, lists, links, tables and images. The server sanitizes HTML and limits the converted Telegram message to 4096 characters. Image uploads require permission to add or change mailings; they accept raster images up to 5 MB and 16 megapixels and re-encode them as PNG without original metadata. Local uploads receive media URLs; S3 uploads receive durable links which resolve to fresh signed URLs. Previously saved editor image links remain valid. There is no separate Django-admin rich-text editor.

The mailing screen shows queued and successful deliveries, attempt counts and error categories. The bot periodically selects due unsent notifications for active linked accounts. Successful sends are marked sent; failed sends remain available for retry. Error categories are stored without provider error text or recipient details.

For Telegram delivery, stored HTML is converted to the formatting supported by the bot's message endpoint. Paragraphs become line breaks, list items and table cells become readable text, and embedded images become links; supported emphasis and links are retained. The stored website HTML is unchanged.

The Telegram bot is a separate process from the website. Browsing, applications, and questionnaires do not depend on a bot response; account linking and delivery of Telegram messages do.
