from django.urls import path
from .views import chat_room,start_chat


urlpatterns = [
    path("", chat_room, name="chats_page"),
    path("<str:room_name>/", chat_room, name="chat_room"),
    path("start/<str:username>/",start_chat, name="start_chat")
]
