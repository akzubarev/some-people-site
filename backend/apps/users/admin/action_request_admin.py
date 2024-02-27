from django.contrib import admin
from related_admin import RelatedFieldAdmin

from apps.users.models import ActionRequest


@admin.register(ActionRequest)
class ActionRequestAdmin(RelatedFieldAdmin):
    raw_id_fields = [
        'user'
    ]
    list_display = [
        'id',
        'user__email',
        'otp',
        'key',
        'data',
        'confirmed',
        'is_used',
        'created_at',
        'expired_at'
    ]
