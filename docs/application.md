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

Django admin is the management interface for game content, nested groups, characters, tags, questions, applications, and mailings. Application management shows status, assigned character, fee, recorded payment, and the player's liked characters. Organizers can select applications as recipients for a mailing.

A mailing holds its text, scheduled time, and recipient selection. Saving a mailing marked ready creates recipient notification records; without a recipient selection, the model uses all users. The bot periodically looks for due, unsent notifications whose users have a linked Telegram chat. It sends the text and marks each successful delivery as sent. Failed sends remain unsent for a later attempt.

The Telegram bot is a separate process from the website. Browsing, applications, and questionnaires do not depend on a bot response; account linking and delivery of Telegram messages do.
