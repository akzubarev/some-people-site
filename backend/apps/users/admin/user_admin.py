from bulk_admin import BulkModelAdmin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from related_admin import RelatedFieldAdmin

from apps.users.models import User
from .forms import UserChangeForm, UserCreationForm


@admin.register(User)
class UserAdmin(BulkModelAdmin, RelatedFieldAdmin, BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_filter = BaseUserAdmin.list_filter + ('country_iso',)

    list_display = [
        'id',
        'email',
        'username',
        'first_name',
        'last_name',
        'created_at',
        'email_active',
        'country_iso',
        'telegram__chat_id'
    ]

    fieldsets = [
        ['Авторизация', {
            'fields': [
                'email',
                'username',
                'password',
                'uuid',
            ]
        }
         ],
        ['Персональная информация', {
            'fields': [
                'last_name',
                'first_name',
                'phone',
                # 'status',
                'avatar',
                'country',
                # 'city',
                'country_iso',
                # 'lat',
                # 'long',
                # 'locale',
            ]
        }
         ],
        ['Настройки', {
            'fields': [
                'groups',
                'is_active',
                'is_staff',
                'is_superuser',
                'email_active',
                # 'location_frozen',
            ]
        }
         ],
        ['Даты', {
            'fields': [
                'last_login',
                'created_at'
            ]
        }
         ],
    ]

    add_fieldsets = [
        [None, {
            'classes': ['wide'],
            'fields': [
                'email',
                # 'username',
                'first_name',
                'last_name',
                'password1',
                'password2',
            ]
        }
         ],
    ]
    search_fields = ['first_name', 'last_name', 'email', 'id',
                     'telegram__chat_id']
    ordering = ["-id"]
    readonly_fields = ['id', 'uuid', 'last_login', 'created_at', 'updated_at']
