"""User admin module."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm

from apps.users.models import User
from .forms import UserCreationForm


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    ordering = ('-id',)
    list_display = [
        'id',
        'email',
        'username',
        'first_name',
        'last_name',
        'telegram_chat_id',
        'telegram_username',
        'created_at',
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
                'avatar',
                'telegram_chat_id',
                'telegram_username',
                'vk',
            ]
        }
         ],
        ['Настройки', {
            'fields': [
                'groups',
                'is_active',
                'is_staff',
                'is_superuser',
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

    # add_fieldsets = [
    #     [None, {
    #         'classes': ['wide'],
    #         'fields': [
    #             'email',
    #             # 'username',
    #             'first_name',
    #             'last_name',
    #             'password1',
    #             'password2',
    #         ]
    #     }
    #      ],
    # ]
    # search_fields = ['first_name', 'last_name', 'email', 'id']
    # ordering = ["-id"]
    readonly_fields = ['id', 'uuid', 'last_login', 'created_at', 'updated_at']
