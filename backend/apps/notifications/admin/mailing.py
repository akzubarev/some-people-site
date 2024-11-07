"""Mailing admin module."""
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin
from django.utils.html import strip_tags

from apps.notifications.models import Mailing


class MailingAdminForm(forms.ModelForm):
    """Mailing admin form."""
    # users = forms.CharField(widget=forms.Textarea)
    # kwargs['widget'] = ManyToManyRawIdWidget(db_field.remote_field, self.admin_site)
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
        'display_text',
        'image',
        'time',
        'ready',
        'created_at'
    ]

    def display_text(self, obj):
        """Displays text without tags."""
        return strip_tags(obj.text)

    form = MailingAdminForm

    search_fields = ['text']

    # def save_related(self, request, form, formsets, change):
    #     from apps.users.models import User
    #     from mixins.enums import MatrixPermissionLevel
    #     # if str(form.data.get('user')) == '1':
    #     #     form.data['user'] = ','.join(set(User.objects.all().values_list('id', flat=True)))
    #     # print(form.instance)

    #     request.POST._mutable = True
    #     request.POST['user'] = ','.join(map(str, set(base_qs.values_list('id', flat=True))))
    #     form.instance.user.clear()
    #     print(form.data, form.instance.user.select_related())

    #     super().save_related(request, form, formsets, change)
