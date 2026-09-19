from asgiref.sync import sync_to_async

from apps.users.models import User
from apps.users.telegram_link import consume_link


@sync_to_async
def user_tg(code: str, username: str, chat_id: str) -> bool:
    return consume_link(code, chat_id, username)


@sync_to_async()
def get_user(chat_id: str) -> User:
    return User.objects.filter(telegram_chat_id=str(chat_id)).first()


@sync_to_async()
def get_users() -> list[User]:
    return list(User.objects.all())
