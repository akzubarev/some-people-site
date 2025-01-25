"""Mailing admin module."""
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin
from django.utils.html import format_html, strip_tags

from apps.notifications.models import Mailing
from apps.users.models import User


class MailingAdminForm(forms.ModelForm):
    """Mailing admin form."""
    text = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Mailing
        fields = '__all__'


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    """Mailing admin."""

    ordering = ('-id',)
    list_display = [
        'id',
        'ready',
        'display_text',
        'image',
        'get_users',
        'time',
        # 'created_at',
    ]

    def display_text(self, obj):
        """Displays text without tags."""
        return strip_tags(obj.text)

    form = MailingAdminForm

    search_fields = ['text']

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        user_ids = request.GET.get('user_ids', '')
        if db_field.name == 'users' and user_ids:
            kwargs['initial'] = User.objects.filter(id__in=user_ids.split(','))
        return super(MailingAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

    def get_users(self, mailing):
        return format_html('<br>'.join([str(user) for user in mailing.users.all()]))
