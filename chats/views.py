from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.db import models
from django.shortcuts import render, redirect
from .models import ChatRoom, Message

User = get_user_model()


@login_required
def start_chat(request, username):

    try:
        other_user = User.objects.get(username=username)
    except User.DoesNotExist:
        messages.error(request, "User doesn't exist")
        return redirect("chats_page")

    if other_user == request.user:
        messages.error(request, "Can not chat with oneself")
        return redirect("chats_page")

    usernames = sorted([request.user.username, other_user.username])
    room_name = f"{usernames[0]}_{usernames[1]}"

    room, created = ChatRoom.objects.get_or_create(
        name=room_name,
        defaults={
            "user1": User.objects.get(username=usernames[0]),
            "user2": User.objects.get(username=usernames[1]),
        },
    )

    return redirect("chat_room", room_name=room_name)


@login_required
def chat_room(request, room_name=None):
    room, messages = None, None
    if room_name is not None:
        try:
            room = ChatRoom.objects.get(name=room_name)
            messages = Message.objects.filter(room=room).order_by("timestamp")
        except ChatRoom.DoesNotExist:
            # create this room
            print("exceptions room doesnt exist")
            # If room doesn't exist
            return redirect("chats_page")

    users = User.objects.exclude(id=request.user.id)

    # Get all rooms for the sidebar
    rooms = ChatRoom.objects.filter(
        models.Q(user1=request.user) | models.Q(user2=request.user)
    ).select_related("user1", "user2")

    return render(
        request,
        "chats.html",
        {
            "users": users,
            "rooms": rooms,
            "current_room": room,
            "messages": messages,
            "room_name": room_name,
        },
    )
