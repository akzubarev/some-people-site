from asgiref.sync import sync_to_async

from ...models import ChatData


async def new_member(update, context):
    chat = update.message['chat']['id']
    new_members = update.message.new_chat_members
    kicked_id = []
    objs = [
        ChatData(chat_id=chat, user_id=member.id)
        for member in new_members if member.id not in kicked_id
    ]
    await sync_to_async(ChatData.objects.bulk_create)(objs)
    await update.message.delete()


async def left_member(update, context):
    await update.message.delete()
