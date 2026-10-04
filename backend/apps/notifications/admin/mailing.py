"""Mailing admin module."""
from django import forms
from django.contrib import admin
from django.utils.html import format_html, strip_tags
from django.urls import reverse_lazy
from django_prose_editor.fields import ProseEditorFormField
from django_prose_editor.widgets import AdminProseEditorWidget

from apps.notifications.models import Mailing
from apps.users.models import User


class MailingEditorWidget(AdminProseEditorWidget):
    @property
    def media(self):
        return super().media + forms.Media(css={'all': [
            'django_prose_editor/overrides.css', 'notifications/editor.css',
        ]})


class MailingAdminForm(forms.ModelForm):
    """Mailing admin form."""
    text = ProseEditorFormField(
        widget=MailingEditorWidget,
        sanitize=True,
        extensions={
            'Bold': True, 'Italic': True, 'Underline': True, 'Strike': True,
            'Subscript': True, 'Superscript': True, 'HardBreak': True,
            'Heading': True, 'BulletList': True, 'OrderedList': True,
            'ListItem': True, 'Blockquote': True, 'Code': True,
            'CodeBlock': True, 'HorizontalRule': True,
            'Link': {'protocols': ['http', 'https', 'mailto', 'tg']},
            'Table': True, 'TableRow': True, 'TableHeader': True, 'TableCell': True,
            'Figure': {'pickerUrl': reverse_lazy('editor-upload')},
            'Image': True, 'Caption': True,
            'History': True, 'HTML': True,
        },
    )

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
    readonly_fields = ('created_at', 'updated_at')

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
