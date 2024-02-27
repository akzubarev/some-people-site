from django.contrib import admin

from ..models import Telegram


# class MailingForm(forms.ModelForm):

#     review_message = forms.CharField(required=False)

#     # def save(self, commit=True):
#     #     review_message = self.cleaned_data.get('review_message', None)
#     #     print(review_message)
#     #     return super().save(commit=commit)

#     class Meta:
#         fields = '__all__'
#         model = Offer

@admin.register(Telegram)
class TelegramAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'username',
        'code',
        'chat_id',
    ]
    raw_id_fields = ['user']

    search_fields = [
        'user__first_name', 'user__last_name', 'user__email', 'user__id',
        'user__telegram__chat_id', 'user__telegram__username'
    ]
