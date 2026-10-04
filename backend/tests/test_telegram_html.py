from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from django.test import SimpleTestCase

from apps.notifications.telegram_html import telegram_html
from bot.jobs.notification import notify_users


class TelegramHTMLTests(SimpleTestCase):
    def convert(self, value):
        return telegram_html(value, base_url='https://example.org/')

    def test_paragraphs_breaks_lists_and_formatting(self):
        self.assertEqual(self.convert('<p><strong>Hello</strong><br>World</p>'
                                     '<ul><li><p>One</p></li><li><p><em>Two</em></p></li></ul>'),
                         '<strong>Hello</strong>\nWorld\n• One\n• <em>Two</em>')

    def test_legacy_formatting_and_entities(self):
        self.assertEqual(self.convert('<b>A &amp; B &lt; C</b>'), '<b>A &amp; B &lt; C</b>')

    def test_images_keep_durable_links_and_tables_keep_content(self):
        output = self.convert('<table><tr><td><p>One</p></td><td><p>Two</p></td></tr></table>'
                              '<img src="/api/media/editor/token/" alt="Portrait">')
        self.assertIn('One | Two', output)
        self.assertIn('<a href="https://example.org/api/media/editor/token/">Portrait</a>', output)
        self.assertNotIn('<table', output)
        self.assertNotIn('<img', output)

    def test_active_html_is_removed(self):
        output = self.convert('<script>attack()</script><p onclick="attack()">Hello</p>'
                              '<a href="javascript:attack()">bad</a>')
        for value in ('script', 'onclick', 'javascript:', 'attack()'):
            self.assertNotIn(value, output)

    async def test_bot_uses_conversion_and_marks_only_successful_delivery(self):
        bot = SimpleNamespace(send_message=AsyncMock())
        notification = SimpleNamespace(id=42, chat_id='synthetic', text='<p>Hello</p>')
        with patch('bot.jobs.notification.db.get_notifications', AsyncMock(return_value=[notification])), \
                patch('bot.jobs.notification.db.mark_notification_sent', AsyncMock()) as mark:
            await notify_users(SimpleNamespace(bot=bot))
            self.assertEqual(bot.send_message.call_args.kwargs['text'], 'Hello')
            mark.assert_awaited_once_with(notification_id=42)

    async def test_failed_delivery_records_only_error_category(self):
        notification = SimpleNamespace(id=42, chat_id='synthetic', text='<p>Hello</p>')
        bot = SimpleNamespace(send_message=AsyncMock(side_effect=RuntimeError('private provider detail')))
        with patch('bot.jobs.notification.db.get_notifications', AsyncMock(return_value=[notification])), \
                patch('bot.jobs.notification.db.mark_notification_sent', AsyncMock()) as sent, \
                patch('bot.jobs.notification.db.mark_notification_failed', AsyncMock()) as failed:
            await notify_users(SimpleNamespace(bot=bot))
            sent.assert_not_awaited()
            failed.assert_awaited_once_with(notification_id=42, error_code='RuntimeError')
