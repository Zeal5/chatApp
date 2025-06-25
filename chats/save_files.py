from django.core.files.base import ContentFile
from .models import Message, ChatRoom
import base64
import uuid


def save_files(room, sender, file_data_base64, filename):
    # Decode base64 file data to bytes
    file_bytes = base64.b64decode(file_data_base64)

    # Create a ContentFile (in-memory file) from bytes
    content_file = ContentFile(file_bytes)

    # Create Message instance with file
    message = Message(
        room=room,
        sender=sender,
        content=filename,  # No text content for file message
    )

    message.file.save(filename, content_file, save=True)
    return message.file.url
