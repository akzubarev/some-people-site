from asgiref.sync import sync_to_async

from apps.users.models import User
from django.core.files import File


@sync_to_async
def user_tg(user_id, chat_id) -> (bool, str):
    user = User.objects.filter(id=int(user_id)).first()

    if user.telegram is not None:
        return False, "Этот телеграм уже подключен"
    user.telegram = chat_id


@sync_to_async
def user_avatar(user_id, photo: File):
    user = User.objects.filter(id=int(user_id)).first()
    if user.avatar is None:
        user.avatar = photo
        user.save()
