from asgiref.sync import sync_to_async

from apps.users.models import User


@sync_to_async
def user_tg(user_uuid: str, username: str, chat_id: str) -> bool:
    """Checks the code from telegram chat against the users uuid."""
    change = False
    user = User.objects.filter(uuid=user_uuid).first()
    if not user:
        raise ValueError('Неверный код.')
    if user.telegram_chat_id is not None:
        change = True
    user.telegram_chat_id = chat_id
    user.telegram_username = username
    user.save()
    return change


@sync_to_async()
def get_user(chat_id: str) -> User:
    return User.objects.filter(telegram_chat_id=str(chat_id)).first()


@sync_to_async()
def get_users() -> list[User]:
    return list(User.objects.all())
