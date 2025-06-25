from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatRoom(models.Model):
    name = models.CharField(max_length=255, unique=True)
    user1 = models.ForeignKey(
        User, related_name="chats_as_user1", on_delete=models.CASCADE
    )
    user2 = models.ForeignKey(
        User, related_name="chats_as_user2", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.name)


class Message(models.Model):
    room = models.ForeignKey(
        ChatRoom, on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to="chat_files/", blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} in {self.room.name}"  # Create your models here.
