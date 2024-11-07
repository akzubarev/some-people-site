"""Notifications app admin package."""
from .mailing import MailingAdmin
from .notification import NotificationAdmin

__all__ = ('MailingAdmin', 'NotificationAdmin')
