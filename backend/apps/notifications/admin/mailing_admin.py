from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin
from django.utils.html import strip_tags

from ..models import Mailing, MailingRecipient


class MailingAdminForm(forms.ModelForm):
    # users = forms.CharField(widget=forms.Textarea)
    # kwargs['widget'] = ManyToManyRawIdWidget(db_field.remote_field, self.admin_site)
    text = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Mailing
        fields = '__all__'


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'locales',
        'entry_level',
        'display_text',
        'created_at'
    ]

    def display_text(self, obj):
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


@admin.register(MailingRecipient)
class MailingRecipientAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "mailing",
        "telegram",
        "email_status",
        # "canceled",
    ]
    list_display_links = [
        "id",
        "user",
        "mailing",
    ]
