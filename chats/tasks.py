from celery import shared_task
from django.contrib.auth import get_user_model
from .models import ChatRoom, Message
from chats.save_files import save_files
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


User = get_user_model()


@shared_task
def save_file_task(
    sender_username, room_name, file_base64, filename, room_group_name, temp_id, mime_type
):
    sender = User.objects.get(username=sender_username)
    room = ChatRoom.objects.get(name=room_name)
    file_url = save_files(room, sender, file_base64, filename)
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        room_group_name,
        {
            "type": "file_uploaded",
            "file_url": file_url,
            "sender": sender_username,
            "filename": filename,
            "temp_id": temp_id,
            "mime_type" : mime_type
        },
    )


@shared_task
def save_message_task(sender_username, room_name, message):
    try:
        sender = User.objects.get(username=sender_username)
        room = ChatRoom.objects.get(name=room_name)
        Message.objects.create(room=room, sender=sender, content=message)
        print("message saved successfully")

    except Exception as e:
        print(f"Error saving message: {e}")
